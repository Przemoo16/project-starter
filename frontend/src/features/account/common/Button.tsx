import {
  ErrorButton as BaseErrorButton,
  ErrorButtonProps as BaseErrorButtonProps,
  SubmitButton as BaseSubmitButton,
  SubmitButtonProps as BaseSubmitButtonProps,
} from '../../../ui-components/Button';

type SubmitButtonProps = Omit<BaseSubmitButtonProps, 'variant' | 'sx'>;
type ErrorButtonProps = Omit<BaseErrorButtonProps, 'variant' | 'sx'>;

export const SubmitButton = (props: SubmitButtonProps) => (
  <BaseSubmitButton variant="contained" sx={{ mt: 2 }} {...props} />
);

export const ErrorButton = (props: ErrorButtonProps) => (
  <BaseErrorButton variant="contained" sx={{ mt: 2 }} {...props} />
);
