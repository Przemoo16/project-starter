import { useTranslation } from 'react-i18next';

import { useAppDispatch, useAppSelector } from '../../../services/store';
import { Paragraph, SubTitle } from '../../../ui-components/Typography';
import { ErrorButton } from '../common/Button';
import { SectionContainer } from '../common/Container';
import { accountActions } from '../store';

export const DeleteAccountSection = () => {
  const { t } = useTranslation();
  const dispatch = useAppDispatch();
  const { deleteAccount } = accountActions;
  const { deleteAccountPending } = useAppSelector(state => state.account);

  const onClick = () => {
    dispatch(deleteAccount());
  };

  return (
    <SectionContainer>
      <SubTitle>{t('account.deleteAccount')}</SubTitle>
      <Paragraph sx={{ mt: 2 }}>{t('account.deleteAccountWarning')}</Paragraph>
      <ErrorButton loading={deleteAccountPending} onClick={onClick}>
        {t('account.deleteAccount')}
      </ErrorButton>
    </SectionContainer>
  );
};
