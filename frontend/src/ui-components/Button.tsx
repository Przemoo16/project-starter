import LoadingButton, { LoadingButtonProps } from '@mui/lab/LoadingButton';

export type SubmitButtonProps = Omit<LoadingButtonProps, 'type'>;

export const SubmitButton = (props: SubmitButtonProps) => (
  <LoadingButton type="submit" {...props} data-testid="submitButton" />
);
