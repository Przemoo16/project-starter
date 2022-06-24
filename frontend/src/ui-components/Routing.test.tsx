import { ReactNode } from 'react';
import { Route, Routes } from 'react-router-dom';

import { render, screen } from '../tests/utils';
import { EnhancedRoute } from './Routing';

interface TestRouterProps {
  element: ReactNode;
}

interface LayoutProps {
  children: ReactNode;
}

const TestRouter = ({ element }: TestRouterProps) => (
  <Routes>
    <Route path="/" element={element} />
    <Route path="/login" element={<>Authentication Route</>} />
    <Route path="/dashboard" element={<>Authenticated Route</>} />
  </Routes>
);

const RouteLayout = ({ children }: LayoutProps) => <div>{children}</div>;
const RouteContent = () => <h1>Home Route</h1>;
const AuthFallbackLayout = ({ children }: LayoutProps) => (
  <div>
    <p>Fallback Layout</p>
    {children}
  </div>
);

describe('EnhancedRoute component', () => {
  it('displays proper route', () => {
    const route = {
      path: '/',
      requiresAuth: false,
      layout: RouteLayout,
      content: RouteContent,
      anonymousOnly: true,
    };
    const authInfo = {
      isAuthPending: false,
      isAuthenticated: false,
      authenticationFallback: '/login',
      authenticatedFallback: '/dashboard',
      authFallbackLayout: AuthFallbackLayout,
    };

    render(<TestRouter element={<EnhancedRoute route={route} authInfo={authInfo} />} />);

    expect(screen.queryByText('Fallback Layout')).not.toBeInTheDocument();
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    expect(screen.queryByText('Authentication Route')).not.toBeInTheDocument();
    expect(screen.queryByText('Authenticated Route')).not.toBeInTheDocument();
    expect(screen.getByText('Home Route')).toBeInTheDocument();
  });

  it('displays app loader with auth fallback layout when auth is pending', () => {
    const route = {
      path: '/',
      requiresAuth: true,
      layout: RouteLayout,
      content: RouteContent,
      anonymousOnly: false,
    };
    const authInfo = {
      isAuthPending: true,
      isAuthenticated: false,
      authenticationFallback: '/login',
      authenticatedFallback: '/dashboard',
      authFallbackLayout: AuthFallbackLayout,
    };

    render(<TestRouter element={<EnhancedRoute route={route} authInfo={authInfo} />} />);

    expect(screen.getByText('Fallback Layout')).toBeInTheDocument();
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
    expect(screen.queryByText('Authentication Route')).not.toBeInTheDocument();
    expect(screen.queryByText('Authenticated Route')).not.toBeInTheDocument();
    expect(screen.queryByText('Home Route')).not.toBeInTheDocument();
  });

  it('redirects to the authentication fallback', () => {
    const route = {
      path: '/',
      requiresAuth: true,
      layout: RouteLayout,
      content: RouteContent,
      anonymousOnly: false,
    };
    const authInfo = {
      isAuthPending: false,
      isAuthenticated: false,
      authenticationFallback: '/login',
      authenticatedFallback: '/dashboard',
      authFallbackLayout: AuthFallbackLayout,
    };

    render(<TestRouter element={<EnhancedRoute route={route} authInfo={authInfo} />} />);

    expect(screen.queryByText('Fallback Layout')).not.toBeInTheDocument();
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    expect(screen.getByText('Authentication Route')).toBeInTheDocument();
    expect(screen.queryByText('Authenticated Route')).not.toBeInTheDocument();
    expect(screen.queryByText('Home Route')).not.toBeInTheDocument();
  });

  it('redirects to the authenticated fallback', () => {
    const route = {
      path: '/',
      requiresAuth: false,
      layout: RouteLayout,
      content: RouteContent,
      anonymousOnly: true,
    };
    const authInfo = {
      isAuthPending: false,
      isAuthenticated: true,
      authenticationFallback: '/login',
      authenticatedFallback: '/dashboard',
      authFallbackLayout: AuthFallbackLayout,
    };

    render(<TestRouter element={<EnhancedRoute route={route} authInfo={authInfo} />} />);

    expect(screen.queryByText('Fallback Layout')).not.toBeInTheDocument();
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    expect(screen.queryByText('Authentication Route')).not.toBeInTheDocument();
    expect(screen.getByText('Authenticated Route')).toBeInTheDocument();
    expect(screen.queryByText('Home Route')).not.toBeInTheDocument();
  });
});
