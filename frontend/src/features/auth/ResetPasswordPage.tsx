import { yupResolver } from '@hookform/resolvers/yup';
import LockResetOutlinedIcon from '@mui/icons-material/LockResetOutlined';
import Button from '@mui/material/Button';
import { useForm } from 'react-hook-form';
import { useTranslation } from 'react-i18next';

import { backend } from '../../services/backend';
import { TextInput } from '../../ui-components/Input';
import { PageContainer } from './common/Container';
import { Form } from './common/Form';
import { Link, LinksContainer } from './common/Link';
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
    <PageContainer icon={LockResetOutlinedIcon} title={t('auth.resetPasswordTitle')}>
      <Form onSubmit={handleSubmit(async values => await backend.resetPassword(values))}>
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
        <LinksContainer>
          <Link to="/login">{t('auth.backToLoginLink')}</Link>
        </LinksContainer>
      </Form>
    </PageContainer>
  );
};

export default ResetPasswordPage;
