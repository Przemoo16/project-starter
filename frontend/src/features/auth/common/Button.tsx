import MuiButton, { ButtonProps } from '@mui/material/Button';
import { Link } from 'react-router-dom';

type ButtonCommonProps = 'variant' | 'fullWidth' | 'sx';
type SubmitButtonProps = Omit<ButtonProps, 'type' | ButtonCommonProps>;
type ButtonWithLinkProps = Omit<ButtonProps<typeof Link>, ButtonCommonProps>;

export const SubmitButton = (props: SubmitButtonProps) => (
  <MuiButton type="submit" variant="contained" fullWidth sx={{ mt: 2 }} {...props} />
);

export const ButtonWithLink = (props: ButtonWithLinkProps) => (
  <MuiButton component={Link} variant="contained" fullWidth sx={{ mt: 3 }} {...props} />
);
