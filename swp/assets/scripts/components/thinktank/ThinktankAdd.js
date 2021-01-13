import {useBreadcrumb} from 'components/Navigation';
import Page from 'components/Page';

import _ from 'utils/i18n';
import {useThinktanksBreadcrumb} from './ThinktankList';
import ThinktankAddForm from './ThinktankAddForm';

const Title = _('New Thinktank');

const ThinktankAdd = ({...props}) => {
    useThinktanksBreadcrumb();
    useBreadcrumb('/thinktank/add/', Title);

    return (
        <Page title={Title}>
            <ThinktankAddForm
                endpoint="/thinktank/"
                redirectURL="/thinktank/"
                {...props}
            />
        </Page>
    );
};

export default ThinktankAdd;
