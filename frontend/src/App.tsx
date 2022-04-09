import './index.css';

import { Route, Routes } from 'react-router-dom';

import { LazyPages } from './features/lazy';
import { useAppSelector } from './services/store';
import { AnonymousLayout } from './ui-components/layouts/AnonymousLayout';
import { AuthLayout } from './ui-components/layouts/AuthLayout';
import { EnhancedRoute, RouteDefinition } from './ui-components/Routing';

const route404: RouteDefinition = {
  path: '*',
  requiresAuth: false,
  layout: AnonymousLayout,
  content: LazyPages.NotFoundPage,
};

const routes: RouteDefinition[] = [
  { path: '/', requiresAuth: false, layout: AnonymousLayout, content: LazyPages.HomePage },
  {
    path: '/login',
    requiresAuth: false,
    layout: AuthLayout,
    content: LazyPages.LoginPage,
  },
  {
    path: '/register',
    requiresAuth: false,
    layout: AuthLayout,
    content: LazyPages.RegisterPage,
  },
  {
    path: '/reset-password',
    requiresAuth: false,
    layout: AuthLayout,
    content: LazyPages.ResetPasswordPage,
  },
  route404,
];

const App = () => {
  const isAuthenticated = useAppSelector(state => !!state.auth.user);
  const isAuthPending = useAppSelector(state => state.auth.pending);

  return (
    <Routes>
      {routes.map((route, i) => (
        <Route
          key={i}
          path={route.path}
          element={
            <EnhancedRoute
              route={route}
              isAuthenticated={isAuthenticated}
              isAuthPending={isAuthPending}
              authFallbackRoute={route404}
            />
          }
        />
      ))}
    </Routes>
  );
};

export default App;
