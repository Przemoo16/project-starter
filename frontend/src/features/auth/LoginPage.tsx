import { yupResolver } from '@hookform/resolvers/yup';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import { SubmitHandler, useForm } from 'react-hook-form';
import { useTranslation } from 'react-i18next';

import { LoginData } from '../../backendTypes';
import { useAppDispatch, useAppSelector } from '../../services/store';
import { PasswordInput, TextInput } from '../common/Input';
import { SubmitButton } from './common/Button';
import { PageContainer } from './common/Container';
import { Form } from './common/Form';
import { Link, LinksContainer } from './common/Link';
import { authActions } from './store';
import { getLoginSchema } from './validation';

const LoginPage = () => {
  const { t } = useTranslation();
  const dispatch = useAppDispatch();
  const { login } = authActions;
  const { loginPending } = useAppSelector(state => state.auth);
  const { control, handleSubmit } = useForm({
    mode: 'onTouched',
    defaultValues: {
      email: '',
      password: '',
    },
    resolver: yupResolver(getLoginSchema()),
  });

  const onSubmit: SubmitHandler<LoginData> = async values => {
    dispatch(login(values));
  };

  return (
    <PageContainer icon={LockOutlinedIcon} title={t('auth.loginTitle')}>
      <Form onSubmit={handleSubmit(onSubmit)}>
        <TextInput
          name="email"
          control={control}
          label={t('auth.email')}
          placeholder="joe@example.com"
          autoComplete="email"
          data-testid="emailInput"
        />
        <PasswordInput
          name="password"
          control={control}
          label={t('auth.password')}
          autoComplete="password"
          data-testid="passwordInput"
        />
        <SubmitButton loading={loginPending}>{t('auth.loginButton')}</SubmitButton>
        <LinksContainer>
          <Link to="/register" data-testid="registerLink">
            {t('auth.registerLink')}
          </Link>
          <Link to="/reset-password" sx={{ mt: 0.5 }} data-testid="resetPasswordLink">
            {t('auth.forgotLink')}
          </Link>
        </LinksContainer>
      </Form>
    </PageContainer>
  );
};

export default LoginPage;
