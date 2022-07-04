import Box from '@mui/material/Box';
import { useTranslation } from 'react-i18next';

import { Paragraph } from '../../ui-components/Typography';
import { Title } from '../common/Typography';

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
      <Title>{t('404.pageNotFound')}</Title>
      <Paragraph align="center" sx={{ mt: 3 }}>
        {t('404.areYouLost')}
      </Paragraph>
    </Box>
  );
};

export default NotFoundPage;
