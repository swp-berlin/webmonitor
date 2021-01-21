import _ from 'utils/i18n';
import {TextInput, NumericInput} from 'components/forms';

import ResolverListForm from '../ResolverListForm';


const ListLabel = _('List');
const ListSelectorLabel = _('List Selector');
const ItemSelectorLabel = _('Item Selector');
const PaginationButtonSelectorLabel = _('Pagination Button Selector');
const MaxPagesLabel = _('Max Pages');


const ListResolverForm = ({form, prefix, level}) => {
    const {control, register, errors} = form;

    return (
        <ResolverListForm form={form} prefix={prefix} level={level}>
            <h2 className="text-lg mb-4">{ListLabel}</h2>
            <input name={`${prefix}.type`} ref={register({required: true})} type="hidden" defaultValue="List" />
            <TextInput
                register={register({required: true})}
                name={`${prefix}.paginator.list_selector`}
                label={ListSelectorLabel}
                errors={errors}
            />
            <TextInput
                register={register({required: true})}
                name={`${prefix}.selector`}
                label={ItemSelectorLabel}
                errors={errors}
            />
            <TextInput
                register={register()}
                name={`${prefix}.paginator.button_selector`}
                label={PaginationButtonSelectorLabel}
                errors={errors}
            />
            <NumericInput
                control={control}
                name={`${prefix}.paginator.max_pages`}
                label={MaxPagesLabel}
                errors={errors}
                defaultValue="1"
                min={1}
                fill
            />
        </ResolverListForm>
    );
};

export default ListResolverForm;
