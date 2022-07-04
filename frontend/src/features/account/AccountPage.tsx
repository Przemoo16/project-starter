import Box from '@mui/material/Box';
import Divider from '@mui/material/Divider';
import { useTranslation } from 'react-i18next';

import { Title } from '../common/Typography';
import { ChangePasswordSection } from './sections/ChangePasswordSection';
import { DeleteAccountSection } from './sections/DeleteAccountSection';
import { UpdateAccountDetailsSection } from './sections/UpdateAccountDetailsSection';

const AccountPage = () => {
  const { t } = useTranslation();

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        width: '100%',
        maxWidth: 500,
      }}
    >
      <Title>{t('ui.account')}</Title>
      <Divider sx={{ width: '100%', my: 5 }} />
      <UpdateAccountDetailsSection />
      <Divider sx={{ width: '100%', my: 5 }} />
      <ChangePasswordSection />
      <Divider sx={{ width: '100%', my: 5 }} />
      <DeleteAccountSection />
      <Divider sx={{ width: '100%', mt: 5 }} />
    </Box>
  );
};

export default AccountPage;
