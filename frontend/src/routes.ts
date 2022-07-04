import { LazyPages } from './features/lazy';
import { AnonymousLayout } from './ui-components/layouts/AnonymousLayout';
import { AuthLayout } from './ui-components/layouts/AuthLayout';
import { DashboardLayout } from './ui-components/layouts/DashboardLayout';
import { RouteDefinition } from './ui-components/Routing';

export const loginRoute: RouteDefinition = {
  title: 'Login',
  path: '/login',
  requiresAuth: false,
  layout: AuthLayout,
  content: LazyPages.LoginPage,
  anonymousOnly: true,
};

export const dashboardRoute: RouteDefinition = {
  title: 'Dashboard',
  path: '/dashboard',
  requiresAuth: true,
  layout: DashboardLayout,
  content: LazyPages.DashboardPage,
  anonymousOnly: false,
};

export const routes: RouteDefinition[] = [
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
    title: 'Account',
    path: '/account',
    requiresAuth: true,
    layout: DashboardLayout,
    content: LazyPages.AccountPage,
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
