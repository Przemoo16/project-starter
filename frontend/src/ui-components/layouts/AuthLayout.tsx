import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import { ReactNode } from 'react';

import heroIcon from '../../assets/icons/hero.svg';
import { Copyright } from '../Copyright';
import { Logo } from '../Icons';

interface Props {
  children: ReactNode;
}

export const AuthLayout = ({ children }: Props) => (
  <Grid container component="main" sx={{ minHeight: '100vh' }}>
    <Grid
      item
      xs={0}
      md={6}
      sx={{
        display: { xs: 'none', md: 'block' },
        backgroundImage: `url(${heroIcon})`,
        backgroundRepeat: 'no-repeat',
        backgroundSize: '80% 80%',
        backgroundPosition: 'center',
      }}
    />
    <Grid
      item
      component={Paper}
      elevation={6}
      square
      xs={12}
      md={6}
      sx={{
        px: 5,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <Box
        component="section"
        sx={{
          width: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          flexGrow: 1,
        }}
      >
        <Logo />
        <Box sx={{ mt: 5 }}>{children}</Box>
      </Box>
      <Box component="footer" sx={{ mb: 3 }}>
        <Copyright />
      </Box>
    </Grid>
  </Grid>
);
