import { Form as BaseForm, FormProps } from '../../../ui-components/Form';
import { ContentContainer } from './Container';

export const Form = (props: FormProps) => (
  <ContentContainer>
    <BaseForm {...props} />
  </ContentContainer>
);
