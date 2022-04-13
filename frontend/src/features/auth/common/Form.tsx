import { Form as BaseForm, FormProps as BaseFormProps } from '../../../ui-components/Form';

type FormProps = Omit<BaseFormProps, 'sx'>;

export const Form = (props: FormProps) => (
  <BaseForm sx={{ width: '100%', maxWidth: 500, mt: 3 }} {...props} />
);
