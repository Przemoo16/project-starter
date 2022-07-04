import { yupResolver } from '@hookform/resolvers/yup';
import AppRegistrationOutlinedIcon from '@mui/icons-material/AppRegistrationOutlined';
import { SubmitHandler, useForm } from 'react-hook-form';
import { useTranslation } from 'react-i18next';

import { RegisterData } from '../../backendTypes';
import { useAppDispatch, useAppSelector } from '../../services/store';
import { PasswordInput, TextInput } from '../common/Input';
import { SubmitButton } from './common/Button';
import { PageContainer } from './common/Container';
import { Form } from './common/Form';
import { Link, LinksContainer } from './common/Link';
import { authActions } from './store';
import { getRegisterSchema } from './validation';

const RegisterPage = () => {
  const { t } = useTranslation();
  const dispatch = useAppDispatch();
  const { register } = authActions;
  const { accountNameMaxLength, accountPasswordMinLength, accountPasswordMaxLength } =
    useAppSelector(state => state.config);
  const { pending } = useAppSelector(state => state.auth);
  const { control, handleSubmit } = useForm({
    mode: 'onTouched',
    defaultValues: {
      name: '',
      email: '',
      password: '',
      repeatPassword: '',
    },
    resolver: yupResolver(
      getRegisterSchema(accountNameMaxLength, accountPasswordMinLength, accountPasswordMaxLength)
    ),
  });

  const onSubmit: SubmitHandler<RegisterData> = async values => {
    dispatch(register(values));
  };

  return (
    <PageContainer
      icon={AppRegistrationOutlinedIcon}
      title={
        <>
          {t('auth.getStarted')}
          <br />
          {t('auth.withFreeAccount')}
        </>
      }
    >
      <Form onSubmit={handleSubmit(onSubmit)}>
        <TextInput
          name="name"
          control={control}
          label={t('account.name')}
          placeholder="Jon Doe"
          autoComplete="name"
          data-testid="nameInput"
        />
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
          data-testid="passwordInput"
        />
        <PasswordInput
          name="repeatPassword"
          control={control}
          label={t('auth.repeatPassword')}
          data-testid="repeatPasswordInput"
        />
        <SubmitButton loading={pending}>{t('auth.getStarted')}</SubmitButton>
        <LinksContainer>
          <Link to="/login" data-testid="loginLink">
            {t('auth.loginLink')}
          </Link>
        </LinksContainer>
      </Form>
    </PageContainer>
  );
};

export default RegisterPage;
