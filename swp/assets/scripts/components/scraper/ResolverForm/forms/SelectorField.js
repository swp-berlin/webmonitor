import {TextInput} from 'components/forms';
import _ from 'utils/i18n';

const SelectorInvalidMessage = _('Please enter a valid css selector');

const isValidSelector = selector => {
    try {
        document.createDocumentFragment().querySelector(selector);
    } catch (SyntaxError) {
        return SelectorInvalidMessage;
    }

    return true;
};


const SelectorField = ({register, required, ...props}) => (
    <TextInput
        register={register({required, validate: {invalid: isValidSelector}})}
        {...props}
    />
);

SelectorField.defaultProps = {
    required: false,
};

export default SelectorField;
