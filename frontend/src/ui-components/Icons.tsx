import Box from '@mui/material/Box';

import logo from '../assets/logo.svg';
import { Link } from './Link';

interface LogoProps {
  size?: number;
}

export const Logo = ({ size = 50 }: LogoProps) => (
  <Link to="/" sx={{ width: '100%' }}>
    <Box
      sx={{
        height: size,
        backgroundImage: `url(${logo})`,
        backgroundRepeat: 'no-repeat',
        backgroundSize: '100% 100%',
        backgroundPosition: 'center',
      }}
    />
  </Link>
);
