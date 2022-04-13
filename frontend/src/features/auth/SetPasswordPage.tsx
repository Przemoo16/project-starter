import { yupResolver } from '@hookform/resolvers/yup';
import KeyOutlinedIcon from '@mui/icons-material/KeyOutlined';
import Avatar from '@mui/material/Avatar';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { useForm } from 'react-hook-form';
import { useTranslation } from 'react-i18next';
import { useParams } from 'react-router-dom';

import { backend } from '../../services/backend';
import { TextInput } from '../../ui-components/Input';
import { Link } from './common/Link';
import { getSetPasswordSchema } from './validation';

const SetPasswordPage = () => {
  const { t } = useTranslation();
  const { key } = useParams();
  const { control, handleSubmit } = useForm({
    mode: 'onTouched',
    defaultValues: {
      password: '',
      repeatPassword: '',
    },
    resolver: yupResolver(getSetPasswordSchema()),
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
        <KeyOutlinedIcon />
      </Avatar>
      <Typography component="h1" variant="h4" align="center" sx={{ mt: 2 }}>
        {t('auth.setPasswordTitle')}
      </Typography>
      <Box
        component="form"
        noValidate
        onSubmit={handleSubmit(
          async values => await backend.setPassword({ ...values, key: key || '' })
        )}
        sx={{ width: '100%', maxWidth: 500, mt: 3 }}
      >
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
          {t('auth.setPasswordButton')}
        </Button>
        <Box
          sx={{
            mt: 2,
          }}
        >
          <Link to="/login">{t('auth.backToLoginLink')}</Link>
        </Box>
      </Box>
    </Box>
  );
};

export default SetPasswordPage;
