import Box from '@mui/material/Box';
import { ReactNode } from 'react';

interface SectionContainerProps {
  children: ReactNode;
}

export const SectionContainer = ({ children }: SectionContainerProps) => (
  <Box
    sx={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'flex-start',
      justifyContent: 'center',
      width: '100%',
    }}
  >
    {children}
  </Box>
);
