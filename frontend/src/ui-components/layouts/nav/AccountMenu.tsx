import LogoutIcon from '@mui/icons-material/Logout';
import PersonIcon from '@mui/icons-material/Person';
import IconButton from '@mui/material/IconButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import { MouseEvent, useState } from 'react';
import { useTranslation } from 'react-i18next';

import { authActions } from '../../../features/auth/store';
import { useAppDispatch, useAppSelector } from '../../../services/store';
import { AccountAvatar } from '../../Avatar';
import { Link } from '../../Link';

export const AccountMenu = () => {
  const { t } = useTranslation();
  const dispatch = useAppDispatch();
  const { logout } = authActions;
  const { account } = useAppSelector(state => state.auth);
  const [anchorEl, setAnchorEl] = useState<HTMLElement | null>(null);

  const handleOpenMenu = (event: MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleCloseMenu = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    dispatch(logout());
  };

  return (
    <>
      <IconButton
        color="inherit"
        onClick={handleOpenMenu}
        aria-label="my account"
        data-testid="accountButton"
      >
        <AccountAvatar account={account} sx={{ width: 35, height: 35 }} />
      </IconButton>
      <Menu
        anchorEl={anchorEl}
        keepMounted
        transformOrigin={{ horizontal: 'right', vertical: 'top' }}
        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
        open={!!anchorEl}
        onClick={handleCloseMenu}
        onClose={handleCloseMenu}
        data-testid="accountMenu"
      >
        <MenuItem component={Link} to="/account" data-testid="accountItem">
          <ListItemIcon>
            <PersonIcon />
          </ListItemIcon>
          {t('ui.account')}
        </MenuItem>
        <MenuItem onClick={handleLogout} data-testid="logoutItem">
          <ListItemIcon>
            <LogoutIcon />
          </ListItemIcon>
          {t('auth.logout')}
        </MenuItem>
      </Menu>
    </>
  );
};
