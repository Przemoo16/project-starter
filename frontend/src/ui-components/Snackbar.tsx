import CloseIcon from '@mui/icons-material/Close';
import { styled } from '@mui/material';
import IconButton from '@mui/material/IconButton';
import { useSnackbar } from 'notistack';
import { SnackbarKey, SnackbarProvider as NotistackProvider } from 'notistack';
import { ReactNode, useEffect, useRef } from 'react';

import { useAppDispatch, useAppSelector } from '../services/store';
import { uiActions } from './store';

interface SnackbarProviderProps {
  maxSnacks?: number;
  children: ReactNode;
}

const MAX_SNACKS = 3;

const StyledSnackbarProvider = styled(NotistackProvider)`
  &.SnackbarItem-variantSuccess {
    background-color: ${props => props.theme.palette.success.main};
  }
  &.SnackbarItem-variantError {
    background-color: ${props => props.theme.palette.error.main};
  }
  &.SnackbarItem-variantInfo {
    background-color: ${props => props.theme.palette.info.main};
  }
`;

export const SnackbarProvider = ({ maxSnacks = MAX_SNACKS, children }: SnackbarProviderProps) => {
  const ref = useRef<NotistackProvider>(null);

  const handleClick = (key: SnackbarKey) => () => {
    ref?.current?.closeSnackbar(key);
  };

  return (
    <StyledSnackbarProvider
      maxSnack={maxSnacks}
      ref={ref}
      action={key => (
        <IconButton
          key={key}
          onClick={handleClick(key)}
          size="small"
          aria-label="close notification"
          color="inherit"
        >
          <CloseIcon fontSize="small" />
        </IconButton>
      )}
    >
      {children}
    </StyledSnackbarProvider>
  );
};

export const Snackbar = () => {
  const notifications = useAppSelector(state => state.ui.notifications);
  const { clearNotifications } = uiActions;
  const dispatch = useAppDispatch();
  const { enqueueSnackbar } = useSnackbar();

  useEffect(() => {
    if (notifications.length) {
      notifications.forEach(({ type, message, duration }) =>
        enqueueSnackbar(message, {
          variant: type,
          anchorOrigin: {
            vertical: 'bottom',
            horizontal: 'right',
          },
          autoHideDuration: duration,
          preventDuplicate: true,
        }),
      );
      dispatch(clearNotifications());
    }
  }, [notifications, enqueueSnackbar, dispatch, clearNotifications]);

  return <></>;
};
