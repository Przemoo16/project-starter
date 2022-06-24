import {
  SubmitButton as BaseSubmitButton,
  SubmitButtonProps as BaseSubmitButtonProps,
} from '../../../ui-components/Buttons';

type SubmitButtonProps = Omit<BaseSubmitButtonProps, 'sx'>;

export const SubmitButton = (props: SubmitButtonProps) => (
  <BaseSubmitButton sx={{ mt: 2 }} {...props} />
);
