import {useEffect, useState} from 'react';
import {Link} from 'react-router-dom';

import ActivationButton from 'components/buttons/ActivationButton';
import {useBreadcrumb} from 'components/Navigation';
import Page from 'components/Page';
import ScraperTable from 'components/scraper/ScraperTable';
import TableActions from 'components/tables/TableActions';

import {useQuery} from 'hooks/query';
import _, {interpolate} from 'utils/i18n';
import {useThinktanksBreadcrumb} from './ThinktankList';


const Loading = _('Loading');
const NewScraperLabel = _('New scraper');
const UniqueLabel = _('Unique on');
const Nbsp = '\u00A0';


const ScraperAddButton = ({...props}) => (
    <Link to="/scraper/add/" className="bp3-button bp3-icon-add" {...props}>
        {NewScraperLabel}
    </Link>
);

const ThinktankDetail = ({id, ...props}) => {
    const endpoint = `/thinktank/${id}/`;
    const {loading, result} = useQuery(endpoint);
    const [isActive, setActive] = useState(false);

    useThinktanksBreadcrumb();
    const label = loading ? interpolate('Thinktank %s', [id], false) : result.data.name;
    useBreadcrumb(endpoint, label);

    useEffect(() => {
        if (!loading) {
            setActive(result.data.is_active);
        }
    }, [loading]);

    if (loading) return Loading;

    const {data: thinktank} = result;
    const {
        unique_field: uniqueField,
        scrapers,
    } = thinktank;

    const onToggle = flag => setActive(flag);
    const actions = [
        <ActivationButton
            key="isActive"
            endpoint={endpoint}
            isActive={isActive}
            onToggle={onToggle}
            disabled={loading}
        />,
    ];

    const subtitle = (
        <span>
            {UniqueLabel}
            {Nbsp}
            <strong>{uniqueField}</strong>
        </span>
    );

    return (
        <Page title={label} subtitle={subtitle} actions={actions}>
            <TableActions>
                <ScraperAddButton />
            </TableActions>

            <ScraperTable items={scrapers} {...props} />
        </Page>
    );
};

export default ThinktankDetail;
