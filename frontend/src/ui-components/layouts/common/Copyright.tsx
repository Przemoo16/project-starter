import Typography from '@mui/material/Typography';
import { useTranslation } from 'react-i18next';

import { useAppSelector } from '../../../services/store';
import { Link } from '../../Link';

export const Copyright = () => {
  const { t } = useTranslation();
  const { appName } = useAppSelector(state => state.config);

  return (
    <Typography variant="body2" color="text.secondary" align="center">
      {`${t('ui.copyright')} © `}
      <Link to="/" color="inherit">
        {appName}
      </Link>
      {` ${new Date().getFullYear()}.`}
    </Typography>
  );
};
