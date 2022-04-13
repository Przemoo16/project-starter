import MuiLink, { LinkProps as MuiLinkProps } from '@mui/material/Link';
import { Link as RouterLink } from 'react-router-dom';

export type LinkProps = MuiLinkProps<typeof RouterLink>;

export const Link = (props: LinkProps) => <MuiLink component={RouterLink} {...props} />;
