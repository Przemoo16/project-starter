import EmailOutlinedIcon from '@mui/icons-material/EmailOutlined';
import { useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useParams } from 'react-router-dom';

import { useAppDispatch, useAppSelector } from '../../services/store';
import { AppLoader } from '../../ui-components/AppLoader';
import { Paragraph } from '../../ui-components/Typography';
import { ContentContainer, PageContainer } from './common/Container';
import { Link, LinksContainer } from './common/Link';
import { authActions } from './store';

const ConfirmEmailPage = () => {
  const { t } = useTranslation();
  const { key } = useParams();
  const dispatch = useAppDispatch();
  const { confirmEmail } = authActions;
  const { confirmEmailPending, errors } = useAppSelector(state => state.auth);

  useEffect(() => {
    dispatch(confirmEmail({ key: key || '' }));
  }, [dispatch, confirmEmail, key]);

  return (
    <PageContainer icon={EmailOutlinedIcon} title={t('auth.confirmEmailTitle')}>
      <ContentContainer>
        {confirmEmailPending && <AppLoader />}
        <Paragraph align="center" sx={{ mt: 2 }} data-testid="confirmEmailMessage">
          {!confirmEmailPending && !errors && t('auth.confirmEmailSuccess')}
          {!confirmEmailPending && errors && t('auth.confirmEmailError')}
        </Paragraph>
        <LinksContainer>
          <Link to="/login" data-testid="loginLink">
            {t('auth.backToLoginLink')}
          </Link>
        </LinksContainer>
      </ContentContainer>
    </PageContainer>
  );
};

export default ConfirmEmailPage;
