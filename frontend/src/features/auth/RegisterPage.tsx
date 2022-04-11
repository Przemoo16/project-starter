import { yupResolver } from '@hookform/resolvers/yup';
import AppRegistrationOutlinedIcon from '@mui/icons-material/AppRegistrationOutlined';
import Avatar from '@mui/material/Avatar';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';
import { useForm } from 'react-hook-form';
import { useTranslation } from 'react-i18next';
import { Link as RouterLink } from 'react-router-dom';

import { backend } from '../../services/backend';
import { TextInput } from '../../ui-components/Input';
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
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <Avatar sx={{ bgcolor: 'secondary.main' }}>
        <AppRegistrationOutlinedIcon />
      </Avatar>
      <Typography component="h1" variant="h4" align="center" sx={{ mt: 2 }}>
        {t('auth.getStarted')}
        <br />
        {t('auth.withFreeAccount')}
      </Typography>
      <Box
        component="form"
        noValidate
        onSubmit={handleSubmit(async values => await backend.signUp(values))}
        sx={{ width: '100%', maxWidth: 500, mt: 3 }}
      >
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
        <Box
          sx={{
            mt: 2,
          }}
        >
          <Link to="/login" component={RouterLink} underline="hover" variant="body2">
            {t('auth.loginLink')}
          </Link>
        </Box>
      </Box>
    </Box>
  );
};

export default RegisterPage;
