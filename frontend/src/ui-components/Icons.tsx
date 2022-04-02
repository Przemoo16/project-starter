import Box from '@mui/material/Box';

import logo from '../assets/logo.svg';

export const Logo = () => (
  <Box
    sx={{
      width: '100%',
      height: 50,
      backgroundImage: `url(${logo})`,
      backgroundRepeat: 'no-repeat',
      backgroundSize: '100% 100%',
      backgroundPosition: 'center',
    }}
  />
);
