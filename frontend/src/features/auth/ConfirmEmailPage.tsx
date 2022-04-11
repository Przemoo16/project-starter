import EmailOutlinedIcon from '@mui/icons-material/EmailOutlined';
import Avatar from '@mui/material/Avatar';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Link as RouterLink } from 'react-router-dom';
import { useParams } from 'react-router-dom';

import { backend } from '../../services/backend';

enum Status {
  PENDING,
  SUCCESS,
  ERROR,
}

const ConfirmEmailPage = () => {
  const { t } = useTranslation();
  const { key } = useParams();
  const [confirmationEmailStatus, setConfirmationEmailStatus] = useState(Status.PENDING);

  useEffect(() => {
    const confirmEmail = async () => {
      try {
        await backend.confirmEmail({ key: key || '' });
        setConfirmationEmailStatus(Status.SUCCESS);
      } catch (e) {
        setConfirmationEmailStatus(Status.ERROR);
      }
    };
    confirmEmail();
  }, [key]);

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <Avatar sx={{ bgcolor: 'secondary.main' }}>
        <EmailOutlinedIcon />
      </Avatar>
      <Typography component="h1" variant="h4" align="center" sx={{ mt: 2 }}>
        {t('auth.confirmEmailTitle')}
      </Typography>
      <Typography align="center" sx={{ mt: 2 }}>
        {confirmationEmailStatus === Status.PENDING && t('auth.confirmEmailPending')}
        {confirmationEmailStatus === Status.SUCCESS && t('auth.confirmEmailSuccess')}
        {confirmationEmailStatus === Status.ERROR && t('auth.confirmEmailError')}
      </Typography>
      <Button to="/login" component={RouterLink} fullWidth variant="contained" sx={{ mt: 3 }}>
        {t('auth.loginButton')}
      </Button>
    </Box>
  );
};

export default ConfirmEmailPage;
