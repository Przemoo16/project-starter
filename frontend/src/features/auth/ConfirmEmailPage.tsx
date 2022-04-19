import EmailOutlinedIcon from '@mui/icons-material/EmailOutlined';
import Typography from '@mui/material/Typography';
import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useParams } from 'react-router-dom';

import { backend } from '../../services/backend';
import { ButtonWithLink } from './common/Button';
import { ContentContainer, PageContainer } from './common/Container';

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
      <ContentContainer>
        <Typography align="center" sx={{ mt: 2 }}>
          {confirmationEmailStatus === Status.PENDING && t('auth.confirmEmailPending')}
          {confirmationEmailStatus === Status.SUCCESS && t('auth.confirmEmailSuccess')}
          {confirmationEmailStatus === Status.ERROR && t('auth.confirmEmailError')}
        </Typography>
        <ButtonWithLink to="/login">{t('auth.loginButton')}</ButtonWithLink>
      </ContentContainer>
    </PageContainer>
  );
};

export default ConfirmEmailPage;
