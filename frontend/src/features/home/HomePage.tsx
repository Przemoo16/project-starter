import { useTranslation } from 'react-i18next';

import { Title } from '../common/Typography';

const HomePage = () => {
  const { t } = useTranslation();

  return <Title>{t('ui.appName')}</Title>;
};

export default HomePage;
