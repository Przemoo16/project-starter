import CloseIcon from '@mui/icons-material/Close';
import IconButton from '@mui/material/IconButton';
import { useSnackbar } from 'notistack';
import { SnackbarKey, SnackbarProvider as NotistackProvider } from 'notistack';
import { ReactNode, useEffect, useRef } from 'react';
import { useDispatch } from 'react-redux';

import { useAppSelector } from '../services/store';
import { uiActions } from './store';

interface SnackbarProviderProps {
  children: ReactNode;
}

const MAX_SNACKS = 3;

export const SnackbarProvider = ({ children }: SnackbarProviderProps) => {
  const ref = useRef<NotistackProvider>(null);

  const onClickHandler = (key: SnackbarKey) => () => {
    ref?.current?.closeSnackbar(key);
  };

  return (
    <NotistackProvider
      maxSnack={MAX_SNACKS}
      ref={ref}
      action={key => (
        <IconButton
          key={key}
          onClick={onClickHandler(key)}
          size="small"
          aria-label="close"
          color="inherit"
        >
          <CloseIcon fontSize="small" />
        </IconButton>
      )}
    >
      {children}
    </NotistackProvider>
  );
};

export const Snackbar = () => {
  const notifications = useAppSelector(state => state.ui.notifications);
  const { clearNotifications } = uiActions;
  const dispatch = useDispatch();
  const { enqueueSnackbar } = useSnackbar();

  useEffect(() => {
    if (notifications.length) {
      notifications.forEach(({ type, message }) =>
        enqueueSnackbar(message, {
          variant: type,
          anchorOrigin: {
            vertical: 'bottom',
            horizontal: 'right',
          },
          autoHideDuration: 4000,
        })
      );
      dispatch(clearNotifications());
    }
  }, [notifications, enqueueSnackbar, dispatch, clearNotifications]);

  return <></>;
};
