import { ComponentType, ReactNode, Suspense } from 'react';
import { Navigate } from 'react-router-dom';

import { AppLoader } from './AppLoader';

type LayoutDefinition = ComponentType<{ children: ReactNode }>;

export interface RouteDefinition {
  path: string;
  requiresAuth: boolean;
  layout: LayoutDefinition;
  content: ComponentType;
  anonymousOnly: boolean;
}

export interface AuthInfo {
  isAuthenticated: boolean;
  isAuthPending: boolean;
  authenticationFallback: string;
  authenticatedFallback: string;
  authFallbackLayout: LayoutDefinition;
}

interface EnhancedRouteProps {
  route: RouteDefinition;
  authInfo: AuthInfo;
}

export const EnhancedRoute = ({ route, authInfo }: EnhancedRouteProps) => {
  const { requiresAuth, anonymousOnly, layout: Layout, content: Content } = route;
  const {
    isAuthPending,
    authFallbackLayout: AuthFallbackLayout,
    isAuthenticated,
    authenticationFallback,
    authenticatedFallback,
  } = authInfo;

  if (isAuthPending && requiresAuth) {
    return (
      <AuthFallbackLayout>
        <AppLoader />
      </AuthFallbackLayout>
    );
  }

  if (requiresAuth && !isAuthenticated) {
    return <Navigate to={authenticationFallback} />;
  }

  if (anonymousOnly && isAuthenticated) {
    return <Navigate to={authenticatedFallback} />;
  }

  return (
    <Layout>
      <Suspense fallback={<AppLoader />}>
        <Content />
      </Suspense>
    </Layout>
  );
};
