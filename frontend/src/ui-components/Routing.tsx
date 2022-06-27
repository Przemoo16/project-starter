import { ComponentType, ReactNode, Suspense, useEffect } from 'react';
import { Navigate } from 'react-router-dom';

import { AppLoader } from './AppLoader';

type LayoutDefinition = ComponentType<{ children: ReactNode }>;

export interface RouteDefinition {
  title: string;
  path: string;
  requiresAuth: boolean;
  layout: LayoutDefinition;
  content: ComponentType;
  anonymousOnly: boolean;
}

export interface AuthInfo {
  isAuthenticated: boolean;
  isAuthPending: boolean;
  authenticationFallback: RouteDefinition;
  authenticatedFallback: RouteDefinition;
}

interface EnhancedRouteProps {
  pageTitle: string;
  route: RouteDefinition;
  authInfo: AuthInfo;
}

export const EnhancedRoute = ({ pageTitle, route, authInfo }: EnhancedRouteProps) => {
  const { title, requiresAuth, anonymousOnly, layout: Layout, content: Content } = route;

  useEffect(() => {
    document.title = title ? `${title} | ${pageTitle}` : pageTitle;
  }, [pageTitle, title]);

  const { isAuthPending, isAuthenticated, authenticationFallback, authenticatedFallback } =
    authInfo;

  const AuthenticationFallbackLayout = authenticationFallback.layout;

  if (isAuthPending && requiresAuth) {
    return (
      <AuthenticationFallbackLayout>
        <AppLoader />
      </AuthenticationFallbackLayout>
    );
  }

  if (requiresAuth && !isAuthenticated) {
    return <Navigate to={authenticationFallback.path} />;
  }

  if (anonymousOnly && isAuthenticated) {
    return <Navigate to={authenticatedFallback.path} />;
  }

  return (
    <Layout>
      <Suspense fallback={<AppLoader />}>
        <Content />
      </Suspense>
    </Layout>
  );
};
