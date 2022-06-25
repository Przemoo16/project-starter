import { ReactNode } from 'react';
import { Route, Routes } from 'react-router-dom';

import { render, screen } from '../tests/utils';
import { AuthInfo, EnhancedRoute, RouteDefinition } from './Routing';

interface TestRouterProps {
  route: RouteDefinition;
  authInfo: AuthInfo;
}
interface LayoutProps {
  children: ReactNode;
}
const PAGE_TITLE = 'Test Page Title';

const RouteLayout = ({ children }: LayoutProps) => <div>{children}</div>;
const HomeRouteContent = () => <h1>Home Content</h1>;

const authenticationFallback = {
  title: 'Authentication',
  path: '/authentication',
  requiresAuth: false,
  layout: ({ children }: LayoutProps) => (
    <div>
      <p>Authentication Layout</p>
      {children}
    </div>
  ),
  content: () => <h1>Authentication Content</h1>,
  anonymousOnly: true,
};

const authenticatedFallback = {
  title: 'Authenticated',
  path: '/authenticated',
  requiresAuth: true,
  layout: RouteLayout,
  content: () => <h1>Authenticated Content</h1>,
  anonymousOnly: false,
};

const TestRouter = ({ route, authInfo }: TestRouterProps) => (
  <Routes>
    <Route
      key={1}
      path={route.path}
      element={<EnhancedRoute pageTitle={PAGE_TITLE} route={route} authInfo={authInfo} />}
    />
    <Route
      key={2}
      path={authenticationFallback.path}
      element={
        <EnhancedRoute pageTitle={PAGE_TITLE} route={authenticationFallback} authInfo={authInfo} />
      }
    />
    <Route
      key={3}
      path={authenticatedFallback.path}
      element={
        <EnhancedRoute pageTitle={PAGE_TITLE} route={authenticatedFallback} authInfo={authInfo} />
      }
    />
  </Routes>
);

describe('EnhancedRoute component', () => {
  it('displays the page title together with the route title', () => {
    const route = {
      title: 'Home',
      path: '/',
      requiresAuth: false,
      layout: RouteLayout,
      content: HomeRouteContent,
      anonymousOnly: true,
    };
    const authInfo = {
      isAuthPending: false,
      isAuthenticated: false,
      authenticationFallback: authenticationFallback,
      authenticatedFallback: authenticatedFallback,
    };

    render(<TestRouter route={route} authInfo={authInfo} />);

    expect(global.window.document.title).toBe(`${route.title} | ${PAGE_TITLE}`);
  });

  it('displays just the page title', () => {
    const route = {
      title: '',
      path: '/',
      requiresAuth: false,
      layout: RouteLayout,
      content: HomeRouteContent,
      anonymousOnly: true,
    };
    const authInfo = {
      isAuthPending: false,
      isAuthenticated: false,
      authenticationFallback: authenticationFallback,
      authenticatedFallback: authenticatedFallback,
    };

    render(<TestRouter route={route} authInfo={authInfo} />);

    expect(global.window.document.title).toBe(PAGE_TITLE);
  });

  it('displays proper route', () => {
    const route = {
      title: 'Home',
      path: '/',
      requiresAuth: false,
      layout: RouteLayout,
      content: HomeRouteContent,
      anonymousOnly: true,
    };
    const authInfo = {
      isAuthPending: false,
      isAuthenticated: false,
      authenticationFallback: authenticationFallback,
      authenticatedFallback: authenticatedFallback,
    };

    render(<TestRouter route={route} authInfo={authInfo} />);

    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    expect(screen.queryByText('Authentication Layout')).not.toBeInTheDocument();
    expect(screen.queryByText('Authentication Content')).not.toBeInTheDocument();
    expect(screen.queryByText('Authenticated Content')).not.toBeInTheDocument();
    expect(screen.getByText('Home Content')).toBeInTheDocument();
  });

  it('displays app loader with auth fallback layout when auth is pending', () => {
    const route = {
      title: 'Home',
      path: '/',
      requiresAuth: true,
      layout: RouteLayout,
      content: HomeRouteContent,
      anonymousOnly: false,
    };
    const authInfo = {
      isAuthPending: true,
      isAuthenticated: false,
      authenticationFallback: authenticationFallback,
      authenticatedFallback: authenticatedFallback,
    };

    render(<TestRouter route={route} authInfo={authInfo} />);

    expect(screen.getByRole('progressbar')).toBeInTheDocument();
    expect(screen.getByText('Authentication Layout')).toBeInTheDocument();
    expect(screen.queryByText('Authentication Content')).not.toBeInTheDocument();
    expect(screen.queryByText('Authenticated Content')).not.toBeInTheDocument();
    expect(screen.queryByText('Home Content')).not.toBeInTheDocument();
  });

  it('redirects to the authentication fallback', () => {
    const route = {
      title: 'Home',
      path: '/',
      requiresAuth: true,
      layout: RouteLayout,
      content: HomeRouteContent,
      anonymousOnly: false,
    };
    const authInfo = {
      isAuthPending: false,
      isAuthenticated: false,
      authenticationFallback: authenticationFallback,
      authenticatedFallback: authenticatedFallback,
    };

    render(<TestRouter route={route} authInfo={authInfo} />);

    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    expect(screen.getByText('Authentication Layout')).toBeInTheDocument();
    expect(screen.getByText('Authentication Content')).toBeInTheDocument();
    expect(screen.queryByText('Authenticated Content')).not.toBeInTheDocument();
    expect(screen.queryByText('Home Content')).not.toBeInTheDocument();
  });

  it('redirects to the authenticated fallback', () => {
    const route = {
      title: 'Home',
      path: '/',
      requiresAuth: false,
      layout: RouteLayout,
      content: HomeRouteContent,
      anonymousOnly: true,
    };
    const authInfo = {
      isAuthPending: false,
      isAuthenticated: true,
      authenticationFallback: authenticationFallback,
      authenticatedFallback: authenticatedFallback,
    };

    render(<TestRouter route={route} authInfo={authInfo} />);

    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    expect(screen.queryByText('Authentication Layout')).not.toBeInTheDocument();
    expect(screen.queryByText('Authentication Content')).not.toBeInTheDocument();
    expect(screen.getByText('Authenticated Content')).toBeInTheDocument();
    expect(screen.queryByText('Home Content')).not.toBeInTheDocument();
  });
});
