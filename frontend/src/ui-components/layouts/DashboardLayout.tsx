import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Toolbar from '@mui/material/Toolbar';
import { ReactNode } from 'react';

import { useAppDispatch, useAppSelector } from '../../services/store';
import { uiActions } from '../store';
import { Copyright } from './common/Copyright';
import { AppBar } from './nav/AppBar';
import { Drawer } from './nav/Drawer';

interface DashboardLayoutProps {
  children: ReactNode;
}

const DRAWER_WIDTH = 240;

export const DashboardLayout = ({ children }: DashboardLayoutProps) => {
  const dispatch = useAppDispatch();
  const { closeDrawer, openDrawer } = uiActions;
  const { drawerOpen } = useAppSelector(state => state.ui);

  const handleOpenDrawer = () => {
    dispatch(openDrawer());
  };

  const handleCloseDrawer = () => {
    dispatch(closeDrawer());
  };

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        minHeight: '100vh',
      }}
    >
      <AppBar onOpen={handleOpenDrawer} drawerWidth={DRAWER_WIDTH} />
      <Drawer open={drawerOpen} onClose={handleCloseDrawer} width={DRAWER_WIDTH} />
      <Container
        component="main"
        maxWidth="lg"
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          flexGrow: 1,
        }}
      >
        <Toolbar />
        <Box
          sx={{
            width: '100%',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            my: 5,
          }}
        >
          {children}
        </Box>
      </Container>
      <Box component="footer" sx={{ mb: 3 }}>
        <Copyright />
      </Box>
    </Box>
  );
};
