import { yupResolver } from '@hookform/resolvers/yup';
import LockResetOutlinedIcon from '@mui/icons-material/LockResetOutlined';
import { SubmitHandler, useForm } from 'react-hook-form';
import { useTranslation } from 'react-i18next';

import { ResetPasswordData } from '../../backendTypes';
import { useAppDispatch } from '../../services/store';
import { TextInput } from '../../ui-components/Input';
import { SubmitButton } from './common/Button';
import { PageContainer } from './common/Container';
import { Form } from './common/Form';
import { Link, LinksContainer } from './common/Link';
import { authActions } from './store';
import { getResetPasswordSchema } from './validation';

const ResetPasswordPage = () => {
  const { t } = useTranslation();
  const dispatch = useAppDispatch();
  const { resetPassword } = authActions;
  const { control, handleSubmit } = useForm({
    mode: 'onTouched',
    defaultValues: {
      email: '',
    },
    resolver: yupResolver(getResetPasswordSchema()),
  });

  const onSubmit: SubmitHandler<ResetPasswordData> = async values => {
    dispatch(resetPassword(values));
  };

  return (
    <PageContainer icon={LockResetOutlinedIcon} title={t('auth.resetPasswordTitle')}>
      <Form onSubmit={handleSubmit(onSubmit)}>
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
        <SubmitButton>{t('auth.sendEmailButton')}</SubmitButton>
        <LinksContainer>
          <Link to="/login" data-testid="loginLink">
            {t('auth.backToLoginLink')}
          </Link>
        </LinksContainer>
      </Form>
    </PageContainer>
  );
};

export default ResetPasswordPage;
