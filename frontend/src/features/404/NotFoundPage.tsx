import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { useTranslation } from 'react-i18next';

const NotFoundPage = () => {
  const { t } = useTranslation();

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <Typography component="h1" variant="h4" align="center">
        {t('404.pageNotFound')}
      </Typography>
      <Typography align="center" sx={{ mt: 3 }}>
        {t('404.areYouLost')}
      </Typography>
    </Box>
  );
};

export default NotFoundPage;
