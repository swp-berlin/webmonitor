import {useEffect, useRef} from 'react';


const ScraperFormErrors = ({form}) => {
    const {errors: {non_field_errors: nonFieldErrors}} = form;
    const nonFieldErrorsRef = useRef(nonFieldErrors);

    useEffect(() => {
        if (nonFieldErrors) {
            nonFieldErrorsRef.current = nonFieldErrors;
            form.clearErrors('non_field_errors');
        }
    }, [form, nonFieldErrors]);

    if (!nonFieldErrorsRef.current) return null;

    return (
        <ul className="my-8">
            {Object.keys(nonFieldErrorsRef.current.types).filter(key => key !== 'ref').map(key => (
                <li key={key} className="text-red-600">{nonFieldErrorsRef.current.types[key]}</li>
            ))}
        </ul>
    );
};

export default ScraperFormErrors;
