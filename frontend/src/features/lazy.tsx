import { lazy } from 'react';

export const LazyPages = {
  HomePage: lazy(() => import('./home/HomePage')),
  LoginPage: lazy(() => import('./auth/LoginPage')),
  RegisterPage: lazy(() => import('./auth/RegisterPage')),
  ResetPasswordPage: lazy(() => import('./auth/ResetPasswordPage')),
  NotFoundPage: lazy(() => import('./404/NotFoundPage')),
};
