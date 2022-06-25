import {
  SubmitButton as BaseSubmitButton,
  SubmitButtonProps as BaseSubmitButtonProps,
} from '../../ui-components/Button';

type SubmitButtonProps = Omit<BaseSubmitButtonProps, 'variant' | 'fullWidth' | 'sx'>;

export const SubmitButton = (props: SubmitButtonProps) => (
  <BaseSubmitButton variant="contained" fullWidth sx={{ mt: 2 }} {...props} />
);
