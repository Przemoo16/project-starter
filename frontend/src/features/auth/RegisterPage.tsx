import { yupResolver } from '@hookform/resolvers/yup';
import AppRegistrationOutlinedIcon from '@mui/icons-material/AppRegistrationOutlined';
import Button from '@mui/material/Button';
import { useForm } from 'react-hook-form';
import { useTranslation } from 'react-i18next';

import { backend } from '../../services/backend';
import { TextInput } from '../../ui-components/Input';
import { PageContainer } from './common/Container';
import { Form } from './common/Form';
import { Link, LinksContainer } from './common/Link';
import { getRegisterSchema } from './validation';

const RegisterPage = () => {
  const { t } = useTranslation();
  const { control, handleSubmit } = useForm({
    mode: 'onTouched',
    defaultValues: {
      name: '',
      email: '',
      password: '',
      repeatPassword: '',
    },
    resolver: yupResolver(getRegisterSchema()),
  });

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
      <Form onSubmit={handleSubmit(async values => await backend.signUp(values))}>
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
        />
        <Button type="submit" fullWidth variant="contained" sx={{ mt: 2 }}>
          {t('auth.getStarted')}
        </Button>
        <LinksContainer>
          <Link to="/login">{t('auth.loginLink')}</Link>
        </LinksContainer>
      </Form>
    </PageContainer>
  );
};

export default RegisterPage;
