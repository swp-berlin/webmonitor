import {Button, Card, Elevation} from '@blueprintjs/core';

import _, {interpolate} from 'utils/i18n';

import {useResolverForm} from './ResolverFormContext';


const UnsupportedTypeLabel = _('Resolver Type %(type)s unsupported');

const ResolverForm = ({form, prefix, level, field = {}, onDelete}) => {
    const {watch, register} = form;
    const name = `${prefix}.type`;
    const type = field.type || watch(name, field.type);
    const Form = useResolverForm(type);

    return (
        <Card className="relative" elevation={Elevation.ONE}>
            <h2 className="text-lg mb-4">{type}</h2>
            {onDelete && <Button small minimal className="absolute top-5 right-5" icon="trash" onClick={onDelete} />}
            <input name={name} ref={register({required: true})} type="hidden" defaultValue={type} />
            {Form ? (
                <Form form={form} prefix={prefix} level={level} field={field} />
            ) : <p>{interpolate(UnsupportedTypeLabel, {type})}</p>}
        </Card>
    );
};

ResolverForm.defaultProps = {
    prefix: '',
    level: 0,
};

export default ResolverForm;
