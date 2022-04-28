import Box from '@mui/material/Box';
import CircularProgress from '@mui/material/CircularProgress';

export const AppLoader = () => (
  <Box
    sx={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
    }}
    data-testid="appLoader"
  >
    <CircularProgress />
  </Box>
);
