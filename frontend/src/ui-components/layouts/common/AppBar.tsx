import MenuIcon from '@mui/icons-material/Menu';
import MuiAppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import IconButton from '@mui/material/IconButton';
import Toolbar from '@mui/material/Toolbar';

import { AccountMenu } from './AccountMenu';

interface AppBarProps {
  onOpenMenu: () => void;
  drawerWidth: number;
}

export const AppBar = ({ onOpenMenu, drawerWidth }: AppBarProps) => (
  <MuiAppBar
    sx={{
      left: {
        lg: drawerWidth,
      },
      width: {
        lg: `calc(100% - ${drawerWidth}px)`,
      },
    }}
  >
    <Toolbar>
      <IconButton
        onClick={onOpenMenu}
        color="inherit"
        aria-label="open menu"
        sx={{
          display: {
            xs: 'inline-flex',
            lg: 'none',
          },
        }}
      >
        <MenuIcon />
      </IconButton>
      <Box sx={{ flexGrow: 1 }} />
      <AccountMenu />
    </Toolbar>
  </MuiAppBar>
);
