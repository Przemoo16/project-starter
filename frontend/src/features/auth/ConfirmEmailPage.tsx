import EmailOutlinedIcon from '@mui/icons-material/EmailOutlined';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Link as RouterLink } from 'react-router-dom';
import { useParams } from 'react-router-dom';

import { backend } from '../../services/backend';
import { PageContainer } from './common/Container';

enum Status {
  PENDING,
  SUCCESS,
  ERROR,
}

const ConfirmEmailPage = () => {
  const { t } = useTranslation();
  const { key } = useParams();
  const [confirmationEmailStatus, setConfirmationEmailStatus] = useState(Status.PENDING);

  useEffect(() => {
    const confirmEmail = async () => {
      try {
        await backend.confirmEmail({ key: key || '' });
        setConfirmationEmailStatus(Status.SUCCESS);
      } catch (e) {
        setConfirmationEmailStatus(Status.ERROR);
      }
    };
    confirmEmail();
  }, [key]);

  return (
    <PageContainer icon={EmailOutlinedIcon} title={t('auth.confirmEmailTitle')}>
      <Typography align="center" sx={{ mt: 2 }}>
        {confirmationEmailStatus === Status.PENDING && t('auth.confirmEmailPending')}
        {confirmationEmailStatus === Status.SUCCESS && t('auth.confirmEmailSuccess')}
        {confirmationEmailStatus === Status.ERROR && t('auth.confirmEmailError')}
      </Typography>
      <Button to="/login" component={RouterLink} fullWidth variant="contained" sx={{ mt: 3 }}>
        {t('auth.loginButton')}
      </Button>
    </PageContainer>
  );
};

export default ConfirmEmailPage;
