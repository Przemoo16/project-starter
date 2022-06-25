import { lazy } from 'react';

export const LazyPages = {
  NotFoundPage: lazy(() => import('./404/NotFoundPage')),
  HomePage: lazy(() => import('./home/HomePage')),
  LoginPage: lazy(() => import('./auth/LoginPage')),
  RegisterPage: lazy(() => import('./auth/RegisterPage')),
  ConfirmEmailPage: lazy(() => import('./auth/ConfirmEmailPage')),
  ResetPasswordPage: lazy(() => import('./auth/ResetPasswordPage')),
  SetPasswordPage: lazy(() => import('./auth/SetPasswordPage')),
  DashboardPage: lazy(() => import('./dashboard/DashboardPage')),
  ProfilePage: lazy(() => import('./account/ProfilePage')),
};
