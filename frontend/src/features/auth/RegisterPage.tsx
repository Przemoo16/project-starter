import { yupResolver } from '@hookform/resolvers/yup';
import AppRegistrationOutlinedIcon from '@mui/icons-material/AppRegistrationOutlined';
import { SubmitHandler, useForm } from 'react-hook-form';
import { useTranslation } from 'react-i18next';

import { RegisterData } from '../../backendTypes';
import { useAppDispatch, useAppSelector } from '../../services/store';
import { TextInput } from '../../ui-components/Input';
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
  const { userNameMaxLength, userPasswordMinLength, userPasswordMaxLength } = useAppSelector(
    state => state.config
  );
  const { control, handleSubmit } = useForm({
    mode: 'onTouched',
    defaultValues: {
      name: '',
      email: '',
      password: '',
      repeatPassword: '',
    },
    resolver: yupResolver(
      getRegisterSchema(userNameMaxLength, userPasswordMinLength, userPasswordMaxLength)
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
          size="small"
          margin="normal"
          fullWidth
          label={t('auth.name')}
          type="text"
          placeholder="Jon Doe"
          autoComplete="name"
          data-testid="nameInput"
        />
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
          data-testid="emailInput"
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
          data-testid="passwordInput"
        />
        <TextInput
          name="repeatPassword"
          control={control}
          size="small"
          margin="normal"
          fullWidth
          label={t('auth.repeatPassword')}
          type="password"
          placeholder="********"
          data-testid="repeatPasswordInput"
        />
        <SubmitButton>{t('auth.getStarted')}</SubmitButton>
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
