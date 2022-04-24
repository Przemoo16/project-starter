import { ReactNode } from 'react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';

import { render, screen } from '../tests/utils';
import { EnhancedRoute } from './Routing';

interface TestRouterProps {
  element: ReactNode;
}

const TestRouter = ({ element }: TestRouterProps) => (
  <MemoryRouter>
    <Routes>
      <Route path="/" element={element} />
      <Route path="/login" element={<>Authentication Route</>} />
      <Route path="/dashboard" element={<>Authenticated Route</>} />
    </Routes>
  </MemoryRouter>
);

describe('EnhancedRoute component', () => {
  it('displays proper route', () => {
    render(
      <TestRouter
        element={
          <EnhancedRoute
            route={{
              path: '/',
              requiresAuth: false,
              layout: ({ children }) => <div>{children}</div>,
              content: () => <>Home Route</>,
              anonymousOnly: true,
            }}
            isAuthPending={false}
            isAuthenticated={false}
            authenticationFallback="/login"
            authenticatedFallback="/dashboard"
          />
        }
      />
    );

    expect(screen.getByText('Home Route')).toBeInTheDocument();
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    expect(screen.queryByText('Authentication Route')).not.toBeInTheDocument();
    expect(screen.queryByText('Authenticated Route')).not.toBeInTheDocument();
  });

  it('displays app loader when auth is pending', () => {
    render(
      <TestRouter
        element={
          <EnhancedRoute
            route={{
              path: '/',
              requiresAuth: true,
              layout: ({ children }) => <div>{children}</div>,
              content: () => <>Home Route</>,
              anonymousOnly: false,
            }}
            isAuthPending
            isAuthenticated={false}
            authenticationFallback="/login"
            authenticatedFallback="/dashboard"
          />
        }
      />
    );

    expect(screen.getByRole('progressbar')).toBeInTheDocument();
    expect(screen.queryByText('Home Route')).not.toBeInTheDocument();
    expect(screen.queryByText('Authentication Route')).not.toBeInTheDocument();
    expect(screen.queryByText('Authenticated Route')).not.toBeInTheDocument();
  });

  it('redirects to the authentication fallback', () => {
    render(
      <TestRouter
        element={
          <EnhancedRoute
            route={{
              path: '/',
              requiresAuth: true,
              layout: ({ children }) => <div>{children}</div>,
              content: () => <>Home Route</>,
              anonymousOnly: false,
            }}
            isAuthPending={false}
            isAuthenticated={false}
            authenticationFallback="/login"
            authenticatedFallback="/dashboard"
          />
        }
      />
    );

    expect(screen.getByText('Authentication Route')).toBeInTheDocument();
    expect(screen.queryByText('Home Route')).not.toBeInTheDocument();
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    expect(screen.queryByText('Authenticated Route')).not.toBeInTheDocument();
  });

  it('redirects to the authenticated fallback', () => {
    render(
      <TestRouter
        element={
          <EnhancedRoute
            route={{
              path: '/',
              requiresAuth: false,
              layout: ({ children }) => <div>{children}</div>,
              content: () => <>Home Route</>,
              anonymousOnly: true,
            }}
            isAuthPending={false}
            isAuthenticated
            authenticationFallback="/login"
            authenticatedFallback="/dashboard"
          />
        }
      />
    );

    expect(screen.getByText('Authenticated Route')).toBeInTheDocument();
    expect(screen.queryByText('Home Route')).not.toBeInTheDocument();
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    expect(screen.queryByText('Authentication Route')).not.toBeInTheDocument();
  });
});
