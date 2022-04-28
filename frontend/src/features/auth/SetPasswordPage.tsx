import { yupResolver } from '@hookform/resolvers/yup';
import KeyOutlinedIcon from '@mui/icons-material/KeyOutlined';
import { SubmitHandler, useForm } from 'react-hook-form';
import { useTranslation } from 'react-i18next';
import { useParams } from 'react-router-dom';

import { SetPasswordData } from '../../backendTypes';
import { useAppDispatch, useAppSelector } from '../../services/store';
import { TextInput } from '../../ui-components/Input';
import { SubmitButton } from './common/Button';
import { PageContainer } from './common/Container';
import { Form } from './common/Form';
import { Link, LinksContainer } from './common/Link';
import { authActions } from './store';
import { getSetPasswordSchema } from './validation';

const SetPasswordPage = () => {
  const { t } = useTranslation();
  const { key } = useParams();
  const { userPasswordMinLength, userPasswordMaxLength } = useAppSelector(state => state.config);
  const dispatch = useAppDispatch();
  const { setPassword } = authActions;
  const { control, handleSubmit } = useForm({
    mode: 'onTouched',
    defaultValues: {
      password: '',
      repeatPassword: '',
    },
    resolver: yupResolver(getSetPasswordSchema(userPasswordMinLength, userPasswordMaxLength)),
  });

  const onSubmit: SubmitHandler<Omit<SetPasswordData, 'key'>> = async values => {
    dispatch(setPassword({ ...values, key: key || '' }));
  };

  return (
    <PageContainer icon={KeyOutlinedIcon} title={t('auth.setPasswordTitle')}>
      <Form onSubmit={handleSubmit(onSubmit)}>
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
        <SubmitButton>{t('auth.setPasswordButton')}</SubmitButton>
        <LinksContainer>
          <Link to="/login" data-testid="loginLink">
            {t('auth.backToLoginLink')}
          </Link>
        </LinksContainer>
      </Form>
    </PageContainer>
  );
};

export default SetPasswordPage;
