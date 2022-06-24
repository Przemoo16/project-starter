import './index.css';

import { Route, Routes } from 'react-router-dom';

import { LazyPages } from './features/lazy';
import { useAppSelector } from './services/store';
import { AnonymousLayout } from './ui-components/layouts/AnonymousLayout';
import { AuthLayout } from './ui-components/layouts/AuthLayout';
import { DashboardLayout } from './ui-components/layouts/DashboardLayout';
import { AuthInfo, EnhancedRoute, RouteDefinition } from './ui-components/Routing';

const loginRoute: RouteDefinition = {
  path: '/login',
  requiresAuth: false,
  layout: AuthLayout,
  content: LazyPages.LoginPage,
  anonymousOnly: true,
};

const dashboardRoute: RouteDefinition = {
  path: '/dashboard',
  requiresAuth: true,
  layout: DashboardLayout,
  content: LazyPages.DashboardPage,
  anonymousOnly: false,
};

const routes: RouteDefinition[] = [
  {
    path: '/',
    requiresAuth: false,
    layout: AnonymousLayout,
    content: LazyPages.HomePage,
    anonymousOnly: false,
  },
  loginRoute,
  {
    path: '/register',
    requiresAuth: false,
    layout: AuthLayout,
    content: LazyPages.RegisterPage,
    anonymousOnly: true,
  },
  {
    path: '/confirm-email/:key',
    requiresAuth: false,
    layout: AuthLayout,
    content: LazyPages.ConfirmEmailPage,
    anonymousOnly: false,
  },
  {
    path: '/reset-password',
    requiresAuth: false,
    layout: AuthLayout,
    content: LazyPages.ResetPasswordPage,
    anonymousOnly: true,
  },
  {
    path: '/set-password/:key',
    requiresAuth: false,
    layout: AuthLayout,
    content: LazyPages.SetPasswordPage,
    anonymousOnly: false,
  },
  dashboardRoute,
  {
    path: '/account/profile',
    requiresAuth: true,
    layout: DashboardLayout,
    content: LazyPages.ProfilePage,
    anonymousOnly: false,
  },
  {
    path: '*',
    requiresAuth: false,
    layout: AnonymousLayout,
    content: LazyPages.NotFoundPage,
    anonymousOnly: false,
  },
];

const App = () => {
  const isAuthenticated = useAppSelector(state => !!state.auth.account);
  const isAuthPending = useAppSelector(state => state.auth.pending);
  const authInfo: AuthInfo = {
    isAuthenticated: isAuthenticated,
    isAuthPending: isAuthPending,
    authenticationFallback: loginRoute.path,
    authenticatedFallback: dashboardRoute.path,
    authFallbackLayout: loginRoute.layout,
  };

  return (
    <Routes>
      {routes.map((route, i) => (
        <Route
          key={i}
          path={route.path}
          element={<EnhancedRoute route={route} authInfo={authInfo} />}
        />
      ))}
    </Routes>
  );
};

export default App;
