import {cloneElement} from 'react';
import {FormGroup} from '@blueprintjs/core';
import cN from 'classnames';

import _ from 'utils/i18n';
import {get, isString} from 'utils/object';

import Errors from 'components/forms/Errors';

const RequiredLabel = _('(required)');

const getErrorMessages = errors => {
    if (!errors) return null;

    if (errors.map) return errors.map((msg, code) => ({code, msg}));

    return Object.keys(errors.types)
        .map(type => ({code: type, msg: errors.types[type]}))
        .filter(error => isString(error.msg));
};

const Field = ({children, id, name, label, labelInfo, errors, hasError, className, disabled, readOnly, ...props}) => {
    const fieldErrors = errors && get(errors, name);
    const intent = (hasError || fieldErrors) ? 'danger' : 'none';
    const {required} = props;

    const errorMessages = getErrorMessages(fieldErrors);

    return (
        <FormGroup
            className={cN(className, 'block text-sm font-medium text-gray-700')}
            label={label}
            labelFor={id || name}
            labelInfo={labelInfo || (required && RequiredLabel)}
            intent={intent}
            helperText={errorMessages && <Errors errors={errorMessages} />}
            disabled={disabled || readOnly}
        >
            {cloneElement(children, {intent, id: id || name, name, disabled, readOnly, ...props})}
        </FormGroup>
    );
};

export default Field;
