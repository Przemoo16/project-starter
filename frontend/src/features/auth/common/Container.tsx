import Avatar from '@mui/material/Avatar';
import Box from '@mui/material/Box';
import SvgIcon from '@mui/material/SvgIcon';
import Typography from '@mui/material/Typography';
import { ReactNode } from 'react';

interface PageContainerProps {
  icon: typeof SvgIcon;
  title: ReactNode;
  children: ReactNode;
}

export const PageContainer = ({ icon: Icon, title, children }: PageContainerProps) => (
  <Box
    sx={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
    }}
  >
    <Avatar sx={{ bgcolor: 'secondary.main' }}>
      <Icon />
    </Avatar>
    <Typography component="h1" variant="h4" align="center" sx={{ mt: 2 }}>
      {title}
    </Typography>
    {children}
  </Box>
);
