import { useTranslation } from 'react-i18next';

import { Link } from '../../Link';
import { Paragraph } from '../../Typography';

export const Copyright = () => {
  const { t } = useTranslation();

  return (
    <Paragraph variant="body2" color="text.secondary" align="center">
      {`${t('ui.copyright')} © `}
      <Link to="/" color="inherit">
        {t('ui.appName')}
      </Link>
      {` ${new Date().getFullYear()}.`}
    </Paragraph>
  );
};
