import LoadingButton, { LoadingButtonProps } from '@mui/lab/LoadingButton';

export type SubmitButtonProps = Omit<LoadingButtonProps, 'type'>;
export type ErrorButtonProps = Omit<LoadingButtonProps, 'color'>;

export const SubmitButton = (props: SubmitButtonProps) => (
  <LoadingButton type="submit" data-testid="submitButton" {...props} />
);

export const ErrorButton = (props: ErrorButtonProps) => (
  <LoadingButton color="error" data-testid="errorButton" {...props} />
);
