import './index.css';

import { useTranslation } from 'react-i18next';
import { Route, Routes } from 'react-router-dom';

import { LazyPages } from './features/lazy';
import { useAppSelector } from './services/store';
import { AnonymousLayout } from './ui-components/layouts/AnonymousLayout';
import { AuthLayout } from './ui-components/layouts/AuthLayout';
import { DashboardLayout } from './ui-components/layouts/DashboardLayout';
import { AuthInfo, EnhancedRoute, RouteDefinition } from './ui-components/Routing';

const loginRoute: RouteDefinition = {
  title: 'Login',
  path: '/login',
  requiresAuth: false,
  layout: AuthLayout,
  content: LazyPages.LoginPage,
  anonymousOnly: true,
};

const dashboardRoute: RouteDefinition = {
  title: 'Dashboard',
  path: '/dashboard',
  requiresAuth: true,
  layout: DashboardLayout,
  content: LazyPages.DashboardPage,
  anonymousOnly: false,
};

const routes: RouteDefinition[] = [
  {
    title: '',
    path: '/',
    requiresAuth: false,
    layout: AnonymousLayout,
    content: LazyPages.HomePage,
    anonymousOnly: true,
  },
  loginRoute,
  {
    title: 'Register',
    path: '/register',
    requiresAuth: false,
    layout: AuthLayout,
    content: LazyPages.RegisterPage,
    anonymousOnly: true,
  },
  {
    title: 'Confirm email',
    path: '/confirm-email/:key',
    requiresAuth: false,
    layout: AuthLayout,
    content: LazyPages.ConfirmEmailPage,
    anonymousOnly: false,
  },
  {
    title: 'Reset password',
    path: '/reset-password',
    requiresAuth: false,
    layout: AuthLayout,
    content: LazyPages.ResetPasswordPage,
    anonymousOnly: true,
  },
  {
    title: 'Set password',
    path: '/set-password/:key',
    requiresAuth: false,
    layout: AuthLayout,
    content: LazyPages.SetPasswordPage,
    anonymousOnly: false,
  },
  dashboardRoute,
  {
    title: 'Profile',
    path: '/account/profile',
    requiresAuth: true,
    layout: DashboardLayout,
    content: LazyPages.ProfilePage,
    anonymousOnly: false,
  },
  {
    title: '404',
    path: '*',
    requiresAuth: false,
    layout: AnonymousLayout,
    content: LazyPages.NotFoundPage,
    anonymousOnly: false,
  },
];

const App = () => {
  const { t } = useTranslation();
  const isAuthenticated = useAppSelector(state => !!state.auth.account);
  const isAuthPending = useAppSelector(state => state.auth.pending);
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
