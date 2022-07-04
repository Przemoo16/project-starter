import LoadingButton, { LoadingButtonProps } from '@mui/lab/LoadingButton';

export type SubmitButtonProps = Omit<LoadingButtonProps, 'type'>;
export type ErrorButtonProps = Omit<LoadingButtonProps, 'color'>;

export const SubmitButton = (props: SubmitButtonProps) => (
  <LoadingButton type="submit" {...props} data-testid="submitButton" />
);

export const ErrorButton = (props: ErrorButtonProps) => (
  <LoadingButton color="error" {...props} data-testid="errorButton" />
);
