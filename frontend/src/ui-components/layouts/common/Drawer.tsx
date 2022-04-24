import DashboardIcon from '@mui/icons-material/Dashboard';
import Divider from '@mui/material/Divider';
import MuiDrawer, { DrawerProps as MuiDrawerProps } from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import { Theme } from '@mui/material/styles';
import Toolbar from '@mui/material/Toolbar';
import useMediaQuery from '@mui/material/useMediaQuery';
import { Link as RouterLink } from 'react-router-dom';

import { Logo } from '../../Icons';

interface DrawerProps extends Pick<MuiDrawerProps, 'open' | 'onClose'> {
  width: number;
}

type DrawerConditionalProps = Pick<DrawerProps, 'open' | 'onClose'> &
  Pick<MuiDrawerProps, 'variant' | 'ModalProps'>;

export const Drawer = ({ open, onClose, width }: DrawerProps) => {
  const largeScreen = useMediaQuery((theme: Theme) => theme.breakpoints.up('lg'));

  const drawerConditionalProps: DrawerConditionalProps = largeScreen
    ? {
        open: true,
        variant: 'permanent',
      }
    : {
        open,
        onClose,
        variant: 'temporary',
        ModalProps: {
          keepMounted: true,
        },
      };

  return (
    <MuiDrawer
      sx={{
        width: width,
        '& .MuiDrawer-paper': {
          width: width,
          boxSizing: 'border-box',
        },
      }}
      data-testid="drawer"
      {...drawerConditionalProps}
    >
      <Toolbar>
        <Logo size={40} />
      </Toolbar>
      <Divider />
      <List component="nav">
        <ListItemButton component={RouterLink} to="/dashboard">
          <ListItemIcon>
            <DashboardIcon />
          </ListItemIcon>
          <ListItemText primary="Dashboard" />
        </ListItemButton>
      </List>
    </MuiDrawer>
  );
};
