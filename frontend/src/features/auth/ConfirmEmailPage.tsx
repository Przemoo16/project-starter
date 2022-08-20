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
  const { token } = useParams();
  const dispatch = useAppDispatch();
  const { confirmEmail } = authActions;
  const { confirmEmailMessage } = useAppSelector(state => state.auth);

  useEffect(() => {
    dispatch(confirmEmail({ token: token || '' }));
  }, []);

  return (
    <PageContainer icon={EmailOutlinedIcon} title={t('auth.confirmEmailTitle')}>
      <ContentContainer>
        {!confirmEmailMessage && <AppLoader />}
        <Paragraph align="center" data-testid="confirmEmailMessage">
          {confirmEmailMessage}
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
