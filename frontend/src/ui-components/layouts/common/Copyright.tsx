import Typography from '@mui/material/Typography';
import { useTranslation } from 'react-i18next';

import { Link } from '../../Link';

export const Copyright = () => {
  const { t } = useTranslation();

  return (
    <Typography variant="body2" color="text.secondary" align="center">
      {`${t('ui.copyright')} © `}
      <Link to="/" color="inherit">
        {t('ui.appName')}
      </Link>
      {` ${new Date().getFullYear()}.`}
    </Typography>
  );
};
