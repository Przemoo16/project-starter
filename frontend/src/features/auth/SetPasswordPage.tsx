import { yupResolver } from '@hookform/resolvers/yup';
import KeyOutlinedIcon from '@mui/icons-material/KeyOutlined';
import { SubmitHandler, useForm } from 'react-hook-form';
import { useTranslation } from 'react-i18next';
import { useParams } from 'react-router-dom';

import { SetPasswordData } from '../../backendTypes';
import { useAppDispatch, useAppSelector } from '../../services/store';
import { PasswordInput } from '../common/Input';
import { SubmitButton } from './common/Button';
import { PageContainer } from './common/Container';
import { Form } from './common/Form';
import { Link, LinksContainer } from './common/Link';
import { authActions } from './store';
import { getSetPasswordSchema } from './validation';

const SetPasswordPage = () => {
  const { t } = useTranslation();
  const { key } = useParams();
  const { accountPasswordMinLength, accountPasswordMaxLength } = useAppSelector(
    state => state.config
  );
  const { setPasswordPending } = useAppSelector(state => state.auth);
  const dispatch = useAppDispatch();
  const { setPassword } = authActions;
  const { control, handleSubmit } = useForm({
    mode: 'onTouched',
    defaultValues: {
      password: '',
      repeatPassword: '',
    },
    resolver: yupResolver(getSetPasswordSchema(accountPasswordMinLength, accountPasswordMaxLength)),
  });

  const onSubmit: SubmitHandler<Omit<SetPasswordData, 'key'>> = async values => {
    dispatch(setPassword({ ...values, key: key || '' }));
  };

  return (
    <PageContainer icon={KeyOutlinedIcon} title={t('auth.setPasswordTitle')}>
      <Form onSubmit={handleSubmit(onSubmit)}>
        <PasswordInput
          name="password"
          control={control}
          label={t('auth.password')}
          data-testid="passwordInput"
        />
        <PasswordInput
          name="repeatPassword"
          control={control}
          label={t('auth.repeatPassword')}
          data-testid="repeatPasswordInput"
        />
        <SubmitButton loading={setPasswordPending}>{t('auth.setPasswordButton')}</SubmitButton>
        <LinksContainer>
          <Link to="/login" data-testid="loginLink">
            {t('auth.backToLoginLink')}
          </Link>
        </LinksContainer>
      </Form>
    </PageContainer>
  );
};

export default SetPasswordPage;
