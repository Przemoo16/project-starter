import AccountCircle from '@mui/icons-material/AccountCircle';
import Logout from '@mui/icons-material/Logout';
import Settings from '@mui/icons-material/Settings';
import IconButton from '@mui/material/IconButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import { MouseEvent, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useDispatch } from 'react-redux';

import { authActions } from '../../../features/auth/store';

export const AccountMenu = () => {
  const { t } = useTranslation();
  const dispatch = useDispatch();
  const [anchorEl, setAnchorEl] = useState<HTMLElement | null>(null);

  const handleOpenMenu = (event: MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleCloseMenu = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    dispatch(authActions.logout());
  };

  return (
    <>
      <IconButton color="inherit" onClick={handleOpenMenu} aria-label="my account">
        <AccountCircle fontSize="large" />
      </IconButton>
      <Menu
        anchorEl={anchorEl}
        keepMounted
        transformOrigin={{ horizontal: 'right', vertical: 'top' }}
        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
        open={!!anchorEl}
        onClose={handleCloseMenu}
      >
        <MenuItem>
          <ListItemIcon>
            <Settings />
          </ListItemIcon>
          {t('ui.settings')}
        </MenuItem>
        <MenuItem onClick={handleLogout}>
          <ListItemIcon>
            <Logout />
          </ListItemIcon>
          {t('auth.logout')}
        </MenuItem>
      </Menu>
    </>
  );
};
