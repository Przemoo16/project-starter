import './index.css';

import { useTranslation } from 'react-i18next';
import { Route, Routes } from 'react-router-dom';

import { dashboardRoute, loginRoute, routes } from './routes';
import { useAppSelector } from './services/store';
import { AuthInfo, EnhancedRoute } from './ui-components/Routing';

const App = () => {
  const { t } = useTranslation();
  const isAuthenticated = useAppSelector(state => !!state.auth.account);
  const isAuthPending = useAppSelector(state => state.auth.loginPending);
  const authInfo: AuthInfo = {
    isAuthenticated: isAuthenticated,
    isAuthPending: isAuthPending,
    authenticationFallback: loginRoute,
    authenticatedFallback: dashboardRoute,
  };

  return (
    <Routes>
      {routes.map((route, i) => (
        <Route
          key={i}
          path={route.path}
          element={<EnhancedRoute pageTitle={t('ui.appName')} route={route} authInfo={authInfo} />}
        />
      ))}
    </Routes>
  );
};

export default App;
