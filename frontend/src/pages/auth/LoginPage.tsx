import { yupResolver } from '@hookform/resolvers/yup';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Avatar from '@mui/material/Avatar';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';
import { useForm } from 'react-hook-form';
import { useTranslation } from 'react-i18next';
import { Link as RouterLink } from 'react-router-dom';

import { TextInput } from '../../ui-components/Input';
import { getLoginSchema } from './validation';

const LoginPage = () => {
  const { t } = useTranslation();
  const { control, handleSubmit } = useForm({
    mode: 'onTouched',
    defaultValues: {
      email: '',
      password: '',
    },
    resolver: yupResolver(getLoginSchema()),
  });

  // TODO: Implement request
  const onSubmit = (data: any) => console.log(data);

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
      <Typography component="h1" variant="h4" sx={{ mt: 1 }}>
        {t('auth.loginTitle')}
      </Typography>
      <Box
        component="form"
        noValidate
        onSubmit={handleSubmit(onSubmit)}
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
          autoComplete="current-password"
        />
        <Button type="submit" fullWidth variant="contained" sx={{ mt: 1 }}>
          {t('auth.loginButton')}
        </Button>
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'flex-start',
            justifyContent: 'center',
            mt: 2.5,
          }}
        >
          <Link to="/register" component={RouterLink} underline="hover" variant="body2">
            {t('auth.registerLink')}
          </Link>
          <Link
            to="/reset-password"
            component={RouterLink}
            underline="hover"
            variant="body2"
            sx={{ mt: 0.5 }}
          >
            {t('auth.forgotLink')}
          </Link>
        </Box>
      </Box>
    </Box>
  );
};

export default LoginPage;
