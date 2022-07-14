import { yupResolver } from '@hookform/resolvers/yup';
import Box from '@mui/material/Box';
import { SubmitHandler, useForm } from 'react-hook-form';
import { useTranslation } from 'react-i18next';

import { LoginData } from '../../../backendTypes';
import { useAppDispatch, useAppSelector } from '../../../services/store';
import { Modal } from '../../../ui-components/Modal';
import { Paragraph, SubTitle } from '../../../ui-components/Typography';
import { PasswordInput } from '../../common/Input';
import { ErrorButton } from '../common/Button';
import { Form } from '../common/Form';
import { accountActions } from '../store';
import { getDeleteAccountSchema } from '../validation';

export const DeleteAccountModal = () => {
  const { t } = useTranslation();
  const dispatch = useAppDispatch();
  const { account } = useAppSelector(state => state.auth);
  const { deleteAccountPending, deleteAccountModalOpen } = useAppSelector(state => state.account);
  const { deleteAccount, closeDeleteAccountModal } = accountActions;
  const { control, handleSubmit, reset } = useForm({
    mode: 'onTouched',
    defaultValues: {
      password: '',
    },
    resolver: yupResolver(getDeleteAccountSchema()),
  });

  const onSubmit: SubmitHandler<Omit<LoginData, 'email'>> = async values => {
    dispatch(deleteAccount({ ...values, email: account?.email || '' }));
  };

  const handleCloseModal = () => {
    dispatch(closeDeleteAccountModal());
    reset({ password: '' });
  };

  return (
    <Modal
      aria-labelledby="delete-account-modal-title"
      aria-describedby="delete-account-modal-description"
      open={deleteAccountModalOpen}
      onClose={handleCloseModal}
      width={500}
    >
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <SubTitle id="delete-account-modal-title" align="center">
          {t('account.deleteAccount')}
        </SubTitle>
        <Paragraph id="delete-account-modal-description" sx={{ mt: 2 }}>
          {t('account.deleteAccountFinalWarning')}
        </Paragraph>
        <Form onSubmit={handleSubmit(onSubmit)}>
          <PasswordInput
            name="password"
            control={control}
            label={t('auth.password')}
            autoComplete="password"
            data-testid="passwordInput"
          />
          <ErrorButton
            type="submit"
            fullWidth
            loading={deleteAccountPending}
            data-testid="confirmDeleteAccountButton"
          >
            {t('account.deleteAccount')}
          </ErrorButton>
        </Form>
      </Box>
    </Modal>
  );
};
