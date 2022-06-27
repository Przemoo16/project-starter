import Typography from '@mui/material/Typography';
import { useTranslation } from 'react-i18next';

const HomePage = () => {
  const { t } = useTranslation();

  return (
    <Typography component="h1" variant="h4" align="center">
      {t('ui.appName')}
    </Typography>
  );
};

export default HomePage;
