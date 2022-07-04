import Avatar from '@mui/material/Avatar';
import Box from '@mui/material/Box';
import SvgIcon from '@mui/material/SvgIcon';
import { ReactNode } from 'react';

import { Title } from '../../common/Typography';

interface PageContainerProps {
  icon: typeof SvgIcon;
  title: ReactNode;
  children: ReactNode;
}

interface ContentContainerProps {
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
    <Title sx={{ mt: 2 }}>{title}</Title>
    {children}
  </Box>
);

export const ContentContainer = ({ children }: ContentContainerProps) => (
  <Box
    sx={{
      width: '100%',
      maxWidth: 500,
      mt: 3,
    }}
  >
    {children}
  </Box>
);
