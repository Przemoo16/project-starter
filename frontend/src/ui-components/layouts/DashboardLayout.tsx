import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Toolbar from '@mui/material/Toolbar';
import { ReactNode, useState } from 'react';

import { AppBar } from './common/AppBar';
import { Copyright } from './common/Copyright';
import { Drawer } from './common/Drawer';

interface DashboardLayoutProps {
  children: ReactNode;
}

const drawerWidth = 240;

export const DashboardLayout = ({ children }: DashboardLayoutProps) => {
  const [openDrawer, setOpenDrawer] = useState(false);

  const handleOpenDrawer = () => {
    setOpenDrawer(true);
  };

  const handleCloseDrawer = () => {
    setOpenDrawer(false);
  };

  return (
    <Box
      sx={{
        display: 'flex',
      }}
    >
      <AppBar onOpenMenu={handleOpenDrawer} drawerWidth={drawerWidth} />
      <Drawer open={openDrawer} onClose={handleCloseDrawer} width={drawerWidth} />
      <Container
        component="main"
        maxWidth="lg"
        sx={{
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
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
            flexGrow: 1,
          }}
        >
          {children}
        </Box>
        <Box component="footer" sx={{ mb: 3 }}>
          <Copyright />
        </Box>
      </Container>
    </Box>
  );
};
