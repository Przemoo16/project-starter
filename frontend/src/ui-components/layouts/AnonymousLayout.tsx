import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import { ReactNode } from 'react';
import { useTranslation } from 'react-i18next';
import { Link as RouterLink } from 'react-router-dom';

import heroIcon from '../../assets/icons/hero.svg';
import { Copyright } from '../Copyright';
import { Logo } from '../Icons';

interface Props {
  children: ReactNode;
}

export const AnonymousLayout = ({ children }: Props) => {
  const { t } = useTranslation();
  return (
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
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <Box
          component="section"
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            flexGrow: 1,
          }}
        >
          <Logo />
          <Box sx={{ my: 5 }}>{children}</Box>
          <Box
            sx={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <Typography>{t('auth.loginTitle')}:</Typography>
            <Button to="/login" component={RouterLink} variant="contained" sx={{ mt: 3 }}>
              {t('auth.loginButton')}
            </Button>
          </Box>
        </Box>
        <Box component="footer" sx={{ mb: 3 }}>
          <Copyright />
        </Box>
      </Grid>
    </Grid>
  );
};
