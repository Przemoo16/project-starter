import { yupResolver } from '@hookform/resolvers/yup';
import KeyOutlinedIcon from '@mui/icons-material/KeyOutlined';
import Button from '@mui/material/Button';
import { useForm } from 'react-hook-form';
import { useTranslation } from 'react-i18next';
import { useParams } from 'react-router-dom';

import { backend } from '../../services/backend';
import { TextInput } from '../../ui-components/Input';
import { PageContainer } from './common/Container';
import { Form } from './common/Form';
import { Link, LinksContainer } from './common/Link';
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
    <PageContainer icon={KeyOutlinedIcon} title={t('auth.setPasswordTitle')}>
      <Form
        onSubmit={handleSubmit(
          async values => await backend.setPassword({ ...values, key: key || '' })
        )}
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
        <LinksContainer>
          <Link to="/login">{t('auth.backToLoginLink')}</Link>
        </LinksContainer>
      </Form>
    </PageContainer>
  );
};

export default SetPasswordPage;
