import Box from '@mui/material/Box';
import { ReactNode } from 'react';

import { Link as BaseLink, LinkProps as BaseLinkProps } from '../../../ui-components/Link';

interface LinksContainerProps {
  children: ReactNode;
}
type LinkProps = Omit<BaseLinkProps, 'underline' | 'variant'>;

export const LinksContainer = ({ children }: LinksContainerProps) => (
  <Box
    sx={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'flex-start',
      justifyContent: 'center',
      mt: 2,
    }}
  >
    {children}
  </Box>
);

export const Link = (props: LinkProps) => <BaseLink underline="hover" variant="body2" {...props} />;
