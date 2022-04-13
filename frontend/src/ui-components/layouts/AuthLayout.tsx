import Box from '@mui/material/Box';
import { ReactNode } from 'react';

import { ContainerWithHero } from './common/Container';

interface AuthLayoutProps {
  children: ReactNode;
}

export const AuthLayout = ({ children }: AuthLayoutProps) => (
  <ContainerWithHero>
    <Box sx={{ width: '100%', mt: 10 }}>{children}</Box>
  </ContainerWithHero>
);
