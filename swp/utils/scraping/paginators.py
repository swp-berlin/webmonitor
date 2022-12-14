import asyncio
from contextlib import asynccontextmanager
from enum import Enum
from typing import Iterable, Iterator

from playwright.async_api import ElementHandle, Page, TimeoutError

from django.utils.translation import gettext_lazy as _

from swp.utils.scraping.context import ScraperContext
from swp.utils.scraping.exceptions import CloudflareError, ResolverError
from swp.utils.scraping.resolvers.base import get_content

REGISTER_OBSERVER = """
    (listElem, itemSelector) => {
        window.observeListPromise = new Promise(resolve => {
            const oldNodes = new Set(listElem.querySelectorAll(itemSelector));
            new MutationObserver((mutationList, observer) => {
                const currentNodes = new Set(listElem.querySelectorAll(itemSelector));

                let newNodes = new Set(currentNodes);
                oldNodes.forEach(node => newNodes.delete(node));

                if (newNodes.size) {
                    resolve(Array.from(newNodes));
                    observer.disconnect();
                }
            }).observe(listElem, {childList: true, subtree: true});
        });
    }
"""

GET_NODE_COUNT = """
    async () => {
        nodes = await window.observeListPromise;
        return nodes.length;
    }
"""

GET_NODE = """
    async i => {
        nodes = await window.observeListPromise;
        return nodes[i];
    }
"""


async def get_nodes_from_result(page: Page):
    length = await page.evaluate(GET_NODE_COUNT)

    return [await page.evaluate_handle(GET_NODE, i) for i in range(length)]


@asynccontextmanager
async def wait_for_nodes(page: Page, list_element: ElementHandle, item_selector: str):
    await list_element.evaluate(REGISTER_OBSERVER, [item_selector])
    yield asyncio.create_task(get_nodes_from_result(page))


def is_cloudflare_protected_page(title: str) -> bool:
    return 'cloudflare' in title.lower()


class Paginator:

    def __init__(self, context: ScraperContext, *, list_selector: str, button_selector: str, item_selector: str = None,
                 max_pages: int = 10,
                 max_per_page: int = None,
                 timeout: int = 5):
        self.context = context
        self.list_selector = list_selector
        self.item_selector = item_selector or '*'
        self.selector = f'{self.list_selector} {self.item_selector}'
        self.button_selector = button_selector
        self.max_pages = max_pages
        self.max_per_page = max_per_page
        self.timeout = timeout

    async def query_list_items(self, page=None) -> Iterable[ElementHandle]:
        page = page or self.context.page

        try:
            # [SWP-144] Precautionary measure against dynamically loaded nodes
            await page.wait_for_selector(self.selector, state='attached', timeout=5000)
        except TimeoutError as exc:
            if is_cloudflare_protected_page(await page.title()):
                raise CloudflareError()

            raise ResolverError(
                _('No elements matching %(selector)s found') % {'selector': self.selector}
            ) from exc

        nodes = await page.query_selector_all(self.selector)

        if not nodes:
            raise ResolverError(
                _('No elements matching %(selector)s found') % {'selector': self.selector}
            )

        return nodes[:self.max_per_page] if self.max_per_page else nodes


class EndlessPaginator(Paginator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def get_next_page(self) -> Iterator[ElementHandle]:
        nodes = await self.query_list_items()

        if not nodes:
            raise ResolverError(
                _('No elements matching %(selector)s found') % {'selector': self.selector}
            )

        yield nodes

        for page_number in range(self.max_pages - 1):
            next_page_link = await self.context.page.query_selector(self.button_selector)

            if not next_page_link:
                break

            list_element = await self.context.page.query_selector(self.list_selector)

            async with wait_for_nodes(self.context.page, list_element, self.item_selector) as get_nodes:
                await next_page_link.click()

                try:
                    nodes = await asyncio.wait_for(get_nodes, timeout=30)
                except asyncio.TimeoutError:
                    raise ResolverError(
                        _('Endless Pagination on page %(page_number)s did not load any new items.') % {
                            'page_number': page_number
                        })

                yield nodes


class PagePaginator(Paginator):

    async def get_next_page(self) -> Iterator[ElementHandle]:
        nodes = await self.query_list_items()

        if not nodes:
            raise ResolverError(
                _('No elements matching %(selector)s found') % {'selector': self.selector}
            )

        yield nodes

        for page_number in range(self.max_pages - 1):
            next_page_link = await self.context.page.query_selector(self.button_selector)

            if not next_page_link:
                break

            href = await get_content(next_page_link, attr='href')

            if not href:
                raise ResolverError(
                    _('Pagination Button matching %(selector)s has no attribute href') % {
                        'selector': self.button_selector
                    }
                )

            await self.nagigate_to_next_page(href, page_number)

            nodes = await self.query_list_items()
            yield nodes

    async def nagigate_to_next_page(self, href, page_number):
        try:
            await self.context.page.goto(href)
        except TimeoutError:
            raise ResolverError(
                _('Timeout while navigating to page %(page_number)s: %(href)s') % {
                    'page_number': page_number,
                    'href': href,
                }
            )


class PaginatorType(Enum):
    Endless = EndlessPaginator
    Page = PagePaginator

    def create(self, context, **config):
        return self.value(context, **config)
