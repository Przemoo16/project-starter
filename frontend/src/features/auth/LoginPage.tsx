import { yupResolver } from '@hookform/resolvers/yup';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import { SubmitHandler, useForm } from 'react-hook-form';
import { useTranslation } from 'react-i18next';
import { useDispatch } from 'react-redux';

import { LoginData } from '../../backendTypes';
import { TextInput } from '../../ui-components/Input';
import { SubmitButton } from './common/Button';
import { PageContainer } from './common/Container';
import { Form } from './common/Form';
import { Link, LinksContainer } from './common/Link';
import { authActions } from './store';
import { getLoginSchema } from './validation';

const LoginPage = () => {
  const { t } = useTranslation();
  const dispatch = useDispatch();
  const { login } = authActions;
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
          size="small"
          margin="normal"
          fullWidth
          label={t('auth.email')}
          type="text"
          placeholder="joe@example.com"
          autoComplete="email"
        />
        <TextInput
          name="password"
          control={control}
          size="small"
          margin="normal"
          fullWidth
          label={t('auth.password')}
          type="password"
          placeholder="********"
          autoComplete="current-password"
        />
        <SubmitButton>{t('auth.loginButton')}</SubmitButton>
        <LinksContainer>
          <Link to="/register">{t('auth.registerLink')}</Link>
          <Link to="/reset-password" sx={{ mt: 0.5 }}>
            {t('auth.forgotLink')}
          </Link>
        </LinksContainer>
      </Form>
    </PageContainer>
  );
};

export default LoginPage;
