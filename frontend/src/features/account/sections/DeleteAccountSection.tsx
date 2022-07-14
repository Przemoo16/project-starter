import { useTranslation } from 'react-i18next';

import { useAppDispatch } from '../../../services/store';
import { Paragraph, SubTitle } from '../../../ui-components/Typography';
import { ErrorButton } from '../common/Button';
import { SectionContainer } from '../common/Container';
import { accountActions } from '../store';
import { DeleteAccountModal } from './DeleteAccountModal';

export const DeleteAccountSection = () => {
  const { t } = useTranslation();
  const dispatch = useAppDispatch();
  const { openDeleteAccountModal } = accountActions;

  const handleOpenModal = () => {
    dispatch(openDeleteAccountModal());
  };

  return (
    <SectionContainer>
      <SubTitle>{t('account.deleteAccount')}</SubTitle>
      <Paragraph sx={{ mt: 2 }}>{t('account.deleteAccountWarning')}</Paragraph>
      <ErrorButton onClick={handleOpenModal} data-testid="deleteAccountButton">
        {t('account.deleteAccount')}
      </ErrorButton>
      <DeleteAccountModal />
    </SectionContainer>
  );
};
