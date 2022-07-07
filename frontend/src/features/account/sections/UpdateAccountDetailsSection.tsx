import { yupResolver } from '@hookform/resolvers/yup';
import { SubmitHandler, useForm } from 'react-hook-form';
import { useTranslation } from 'react-i18next';

import { UpdateAccountDetailsData } from '../../../backendTypes';
import { useAppDispatch, useAppSelector } from '../../../services/store';
import { AccountAvatar } from '../../../ui-components/Avatar';
import { SubTitle } from '../../../ui-components/Typography';
import { TextInput } from '../../common/Input';
import { SubmitButton } from '../common/Button';
import { SectionContainer } from '../common/Container';
import { Form } from '../common/Form';
import { accountActions } from '../store';
import { getUpdateAccountDetailsSchema } from '../validation';

export const UpdateAccountDetailsSection = () => {
  const { t } = useTranslation();
  const dispatch = useAppDispatch();
  const { updateAccountDetails } = accountActions;
  const { accountNameMaxLength } = useAppSelector(state => state.config);
  const { account } = useAppSelector(state => state.auth);
  const { updateAccountDetailsPending } = useAppSelector(state => state.account);
  const { control, handleSubmit } = useForm({
    mode: 'onTouched',
    defaultValues: {
      name: account?.name || '',
    },
    resolver: yupResolver(getUpdateAccountDetailsSchema(accountNameMaxLength)),
  });

  const onSubmit: SubmitHandler<UpdateAccountDetailsData> = async values => {
    dispatch(updateAccountDetails(values));
  };

  return (
    <SectionContainer>
      <SubTitle>{t('account.updateAccountDetails')}</SubTitle>
      <AccountAvatar account={account} sx={{ width: 100, height: 100, mt: 2 }} />
      <Form onSubmit={handleSubmit(onSubmit)}>
        <TextInput
          name="name"
          control={control}
          label={t('account.name')}
          placeholder="Jon Doe"
          autoComplete="name"
          data-testid="nameInput"
        />
        <SubmitButton
          loading={updateAccountDetailsPending}
          data-testid="updateAccountDetailsButton"
        >
          {t('account.updateAccountDetails')}
        </SubmitButton>
      </Form>
    </SectionContainer>
  );
};
