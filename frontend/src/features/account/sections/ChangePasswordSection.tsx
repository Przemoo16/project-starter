import { yupResolver } from '@hookform/resolvers/yup';
import { useEffect } from 'react';
import { SubmitHandler, useForm } from 'react-hook-form';
import { useTranslation } from 'react-i18next';

import { ChangePasswordData } from '../../../backendTypes';
import { useAppDispatch, useAppSelector } from '../../../services/store';
import { SubTitle } from '../../../ui-components/Typography';
import { PasswordInput } from '../../common/Input';
import { SubmitButton } from '../common/Button';
import { SectionContainer } from '../common/Container';
import { Form } from '../common/Form';
import { accountActions } from '../store';
import { getChangePasswordSchema } from '../validation';

export const ChangePasswordSection = () => {
  const { t } = useTranslation();
  const dispatch = useAppDispatch();
  const { changePassword } = accountActions;
  const { accountPasswordMinLength, accountPasswordMaxLength } = useAppSelector(
    state => state.config
  );
  const { changePasswordPending } = useAppSelector(state => state.account);
  const { control, handleSubmit, reset, formState } = useForm({
    mode: 'onTouched',
    defaultValues: {
      currentPassword: '',
      newPassword: '',
      repeatNewPassword: '',
    },
    resolver: yupResolver(
      getChangePasswordSchema(accountPasswordMinLength, accountPasswordMaxLength)
    ),
  });

  const onSubmit: SubmitHandler<ChangePasswordData> = async values => {
    dispatch(changePassword(values));
  };

  useEffect(() => {
    if (formState.isSubmitSuccessful) {
      reset({ currentPassword: '', newPassword: '', repeatNewPassword: '' });
    }
  }, [formState.isSubmitSuccessful]);

  return (
    <SectionContainer>
      <SubTitle>{t('account.changePassword')}</SubTitle>
      <Form onSubmit={handleSubmit(onSubmit)}>
        <PasswordInput
          name="currentPassword"
          control={control}
          label={t('account.currentPassword')}
          data-testid="currentPasswordInput"
        />
        <PasswordInput
          name="newPassword"
          control={control}
          label={t('account.newPassword')}
          data-testid="newPasswordInput"
        />
        <PasswordInput
          name="repeatNewPassword"
          control={control}
          label={t('account.repeatNewPassword')}
          data-testid="repeatNewPasswordInput"
        />
        <SubmitButton loading={changePasswordPending} data-testid="changePasswordButton">
          {t('account.changePassword')}
        </SubmitButton>
      </Form>
    </SectionContainer>
  );
};
