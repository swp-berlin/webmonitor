import {HTMLTable} from '@blueprintjs/core';

import _ from 'utils/i18n';
import EmptyRow from 'components/tables/EmptyRow';
import ThinktankFilterRow from './ThinktankFilterRow';


const NameLabel = _('Name');
const FilterLabel = _('Filter');
const PublicationCountLabel = _('Publications');
const NewPublicationCountLabel = _('New');


const FilterRows = ({monitorID, items}) => (
    items.map(
        ({id, name, filters, publication_count: publicationCount, new_publication_count: newPublicationCount}) => (
            <ThinktankFilterRow
                key={id}
                monitorID={monitorID}
                id={id}
                name={name}
                filters={filters}
                publicationCount={publicationCount}
                newPublicationCount={newPublicationCount}
            />
        ),
    )
);

const ThinktankFilterTable = ({items, monitorID, ...props}) => (
    <HTMLTable className="filter-table w-full table-fixed my-4" bordered {...props}>
        <thead className="bg-gray-300">
            <tr>
                <th className="w-1/2">{NameLabel}</th>
                <th>{FilterLabel}</th>
                <th className="text-right">{PublicationCountLabel}</th>
                <th className="text-right">{NewPublicationCountLabel}</th>
            </tr>
        </thead>
        <tbody>
            {items.length ? <FilterRows monitorID={monitorID} items={items} /> : <EmptyRow colSpan={4} />}
        </tbody>
    </HTMLTable>
);

export default ThinktankFilterTable;
