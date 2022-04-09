import './i18n';

import CssBaseline from '@mui/material/CssBaseline';
import { ThemeProvider } from '@mui/material/styles';
import React from 'react';
import ReactDOM from 'react-dom';
import { Provider as ReduxProvider } from 'react-redux';
import { unstable_HistoryRouter as HistoryRouter } from 'react-router-dom';

import App from './App';
import { history } from './services/history';
import { createStore } from './services/store';
import { theme } from './ui-components/theme';

const store = createStore();

ReactDOM.render(
  <React.StrictMode>
    <ReduxProvider store={store}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <HistoryRouter history={history}>
          <App />
        </HistoryRouter>
      </ThemeProvider>
    </ReduxProvider>
  </React.StrictMode>,
  document.getElementById('root')
);
