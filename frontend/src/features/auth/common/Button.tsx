import MuiButton, { ButtonProps } from '@mui/material/Button';

type SubmitButtonProps = Omit<ButtonProps, 'type' | 'variant' | 'fullWidth' | 'sx'>;

export const SubmitButton = (props: SubmitButtonProps) => (
  <MuiButton
    type="submit"
    variant="contained"
    fullWidth
    sx={{ mt: 2 }}
    {...props}
    data-testid="submitButton"
  />
);
