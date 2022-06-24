import MuiLink, { LinkProps as MuiLinkProps } from '@mui/material/Link';
import { forwardRef } from 'react';
import { Link as RouterLink } from 'react-router-dom';

export type LinkProps = MuiLinkProps<typeof RouterLink>;

export const Link = forwardRef<HTMLAnchorElement, LinkProps>((props, ref) => (
  <MuiLink component={RouterLink} ref={ref} {...props} />
));
