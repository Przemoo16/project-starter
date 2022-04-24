import { ComponentType, ReactNode, Suspense } from 'react';
import { Navigate } from 'react-router-dom';

import { AppLoader } from './AppLoader';

export interface RouteDefinition {
  path: string;
  requiresAuth: boolean;
  layout: ComponentType<{ children: ReactNode }>;
  content: ComponentType;
  anonymousOnly: boolean;
}

interface EnhancedRouteProps {
  route: RouteDefinition;
  isAuthenticated: boolean;
  isAuthPending: boolean;
  authenticationFallback: string;
  authorizedFallback: string;
}

export const EnhancedRoute = ({
  route,
  isAuthPending,
  isAuthenticated,
  authenticationFallback,
  authorizedFallback,
}: EnhancedRouteProps) => {
  let { layout: Layout, content: Content, requiresAuth, anonymousOnly } = route;

  if (isAuthPending && requiresAuth) {
    return <AppLoader />;
  }

  if (requiresAuth && !isAuthenticated) {
    return <Navigate to={authenticationFallback} />;
  }

  if (anonymousOnly && isAuthenticated) {
    return <Navigate to={authorizedFallback} />;
  }

  return (
    <Layout>
      <Suspense fallback={<AppLoader />}>
        <Content />
      </Suspense>
    </Layout>
  );
};
