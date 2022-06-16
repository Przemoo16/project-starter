import LoadingButton, { LoadingButtonProps } from '@mui/lab/LoadingButton';

type SubmitButtonProps = Omit<LoadingButtonProps, 'type' | 'variant' | 'fullWidth' | 'sx'>;

export const SubmitButton = (props: SubmitButtonProps) => (
  <LoadingButton
    type="submit"
    variant="contained"
    fullWidth
    sx={{ mt: 2 }}
    {...props}
    data-testid="submitButton"
  />
);
