from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


DEFAULT_ERROR = ''  # FIXME


class ScraperError(models.Model):
    """
    Error encountered during scraping.
    """

    scraper = models.ForeignKey(
        'swp.Scraper',
        on_delete=models.CASCADE,
        related_name='errors',
        verbose_name=_('scraper'),
    )

    code = models.CharField(_('error code'), max_length=8, default=DEFAULT_ERROR)
    message = models.TextField(_('message'))
    timestamp = models.DateTimeField(_('timestamp'), default=timezone.now, editable=False)

    class Meta:
        get_latest_by = 'timestamp'
        verbose_name = _('scraping error')
        verbose_name_plural = _('scraping errors')

    def __str__(self) -> str:
        return self.code or self.message