import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';
import { useTranslation } from 'react-i18next';
import { Link as RouterLink } from 'react-router-dom';

export const Copyright = () => {
  const { t } = useTranslation();
  return (
    <Typography variant="body2" color="text.secondary" align="center">
      {`${t('common.copyright')} © `}
      <Link color="inherit" to="/" component={RouterLink}>
        {process.env.REACT_APP_NAME}
      </Link>
      {` ${new Date().getFullYear()}.`}
    </Typography>
  );
};
