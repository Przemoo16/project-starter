import EmailOutlinedIcon from '@mui/icons-material/EmailOutlined';
import Typography from '@mui/material/Typography';
import { useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useDispatch } from 'react-redux';
import { useParams } from 'react-router-dom';

import { useAppSelector } from '../../services/store';
import { AppLoader } from '../../ui-components/AppLoader';
import { ButtonWithLink } from './common/Button';
import { ContentContainer, PageContainer } from './common/Container';
import { authActions } from './store';

const ConfirmEmailPage = () => {
  const { t } = useTranslation();
  const { key } = useParams();
  const dispatch = useDispatch();
  const { confirmEmail } = authActions;
  const { confirmEmailPending, confirmEmailSuccess } = useAppSelector(state => state.auth);

  useEffect(() => {
    dispatch(confirmEmail({ key: key || '' }));
  }, [dispatch, confirmEmail, key]);

  return (
    <PageContainer icon={EmailOutlinedIcon} title={t('auth.confirmEmailTitle')}>
      <ContentContainer>
        {confirmEmailPending && <AppLoader />}
        <Typography align="center" sx={{ mt: 2 }}>
          {!confirmEmailPending && confirmEmailSuccess && t('auth.confirmEmailSuccess')}
          {!confirmEmailPending && !confirmEmailSuccess && t('auth.confirmEmailError')}
        </Typography>
        <ButtonWithLink to="/login">{t('auth.loginButton')}</ButtonWithLink>
      </ContentContainer>
    </PageContainer>
  );
};

export default ConfirmEmailPage;
