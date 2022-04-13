import { yupResolver } from '@hookform/resolvers/yup';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Avatar from '@mui/material/Avatar';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { useForm } from 'react-hook-form';
import { useTranslation } from 'react-i18next';
import { useDispatch } from 'react-redux';

import { TextInput } from '../../ui-components/Input';
import { Link } from './common/Link';
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
        <LockOutlinedIcon />
      </Avatar>
      <Typography component="h1" variant="h4" align="center" sx={{ mt: 2 }}>
        {t('auth.loginTitle')}
      </Typography>
      <Box
        component="form"
        noValidate
        onSubmit={handleSubmit(async values => dispatch(login(values)))}
        sx={{ width: '100%', maxWidth: 500, mt: 3 }}
      >
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
        <Button type="submit" fullWidth variant="contained" sx={{ mt: 2 }}>
          {t('auth.loginButton')}
        </Button>
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'flex-start',
            justifyContent: 'center',
            mt: 2,
          }}
        >
          <Link to="/register">{t('auth.registerLink')}</Link>
          <Link to="/reset-password" sx={{ mt: 0.5 }}>
            {t('auth.forgotLink')}
          </Link>
        </Box>
      </Box>
    </Box>
  );
};

export default LoginPage;
