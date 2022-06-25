import { yupResolver } from '@hookform/resolvers/yup';
import { SubmitHandler, useForm } from 'react-hook-form';
import { useTranslation } from 'react-i18next';

import { UpdateAccountData } from '../../backendTypes';
import { useAppDispatch, useAppSelector } from '../../services/store';
import { Form } from '../../ui-components/Form';
import { SubmitButton } from '../common/Button';
import { TextInput } from '../common/Input';
import { accountActions } from './store';
import { getUpdateAccountSchema } from './validation';

const ProfilePage = () => {
  const { t } = useTranslation();
  const dispatch = useAppDispatch();
  const { updateAccount } = accountActions;
  const { accountNameMaxLength } = useAppSelector(state => state.config);
  const { account } = useAppSelector(state => state.auth);
  const { pending } = useAppSelector(state => state.account);
  const { control, handleSubmit } = useForm({
    mode: 'onTouched',
    defaultValues: {
      name: account?.name || '',
    },
    resolver: yupResolver(getUpdateAccountSchema(accountNameMaxLength)),
  });

  const onSubmit: SubmitHandler<UpdateAccountData> = async values => {
    dispatch(updateAccount(values));
  };

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <TextInput
        name="name"
        control={control}
        label={t('account.name')}
        placeholder="Jon Doe"
        autoComplete="name"
        data-testid="nameInput"
      />
      <SubmitButton loading={pending}>{t('account.updateAccount')}</SubmitButton>
    </Form>
  );
};

export default ProfilePage;
