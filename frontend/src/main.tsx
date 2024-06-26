import './i18n';

import CssBaseline from '@mui/material/CssBaseline';
import { ThemeProvider } from '@mui/material/styles';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { Provider as ReduxProvider } from 'react-redux';
import { unstable_HistoryRouter as HistoryRouter } from 'react-router-dom';

import App from './App';
import { history } from './services/history';
import { createStore } from './services/store';
import { Snackbar, SnackbarProvider } from './ui-components/Snackbar';
import { theme } from './ui-components/theme';

const store = createStore();

createRoot(document.getElementById('root') as HTMLElement).render(
  <StrictMode>
    <ReduxProvider store={store}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <HistoryRouter history={history}>
          <SnackbarProvider>
            <App />
            <Snackbar />
          </SnackbarProvider>
        </HistoryRouter>
      </ThemeProvider>
    </ReduxProvider>
  </StrictMode>,
);
