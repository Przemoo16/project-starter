import LoadingButton, { LoadingButtonProps } from '@mui/lab/LoadingButton';

export type SubmitButtonProps = Omit<LoadingButtonProps, 'type' | 'variant' | 'fullWidth'>;

export const SubmitButton = (props: SubmitButtonProps) => (
  <LoadingButton
    type="submit"
    variant="contained"
    fullWidth
    {...props}
    data-testid="submitButton"
  />
);
