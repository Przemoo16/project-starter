import { yupResolver } from '@hookform/resolvers/yup';
import LockResetOutlinedIcon from '@mui/icons-material/LockResetOutlined';
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
import { getResetPasswordSchema } from './validation';

const ResetPasswordPage = () => {
  const { t } = useTranslation();
  const { control, handleSubmit } = useForm({
    mode: 'onTouched',
    defaultValues: {
      email: '',
    },
    resolver: yupResolver(getResetPasswordSchema()),
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
        <LockResetOutlinedIcon />
      </Avatar>
      <Typography component="h1" variant="h4" align="center" sx={{ mt: 2 }}>
        {t('auth.resetPasswordTitle')}
      </Typography>
      <Box
        component="form"
        noValidate
        onSubmit={handleSubmit(async values => await backend.requestResetPassword(values))}
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
        <Button type="submit" fullWidth variant="contained" sx={{ mt: 2 }}>
          {t('auth.sendEmailButton')}
        </Button>
        <Box
          sx={{
            mt: 2,
          }}
        >
          <Link to="/login" component={RouterLink} underline="hover" variant="body2">
            {t('auth.backToLoginLink')}
          </Link>
        </Box>
      </Box>
    </Box>
  );
};

export default ResetPasswordPage;
