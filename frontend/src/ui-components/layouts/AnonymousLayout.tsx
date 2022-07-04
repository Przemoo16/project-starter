import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import { ReactNode } from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';

import { Paragraph } from '../../ui-components/Typography';
import { ContainerWithHero } from './common/Container';

interface AnonymousLayoutProps {
  children: ReactNode;
}

export const AnonymousLayout = ({ children }: AnonymousLayoutProps) => {
  const { t } = useTranslation();
  return (
    <ContainerWithHero>
      <Box sx={{ width: '100%', mt: 10, mb: 5 }}>{children}</Box>
      <Box
        sx={{
          width: '100%',
          maxWidth: 500,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <Paragraph align="center">{t('auth.loginTitle')}:</Paragraph>
        <Button
          to="/login"
          component={Link}
          fullWidth
          variant="contained"
          sx={{ mt: 2 }}
          data-testid="loginButton"
        >
          {t('auth.loginButton')}
        </Button>
      </Box>
    </ContainerWithHero>
  );
};
