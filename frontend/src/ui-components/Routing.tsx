import { Suspense } from 'react';

import { AppLoader } from './AppLoader';

export interface RouteDefinition {
  path: string;
  requiresAuth: boolean;
  layout: React.ComponentType<{ children: React.ReactNode }>;
  content: React.ComponentType;
}

interface EnhancedRouteProps {
  route: RouteDefinition;
  isAuthenticated: boolean;
  isAuthPending: boolean;
  authFallbackRoute: RouteDefinition;
}

export const EnhancedRoute = ({
  route,
  isAuthPending,
  isAuthenticated,
  authFallbackRoute,
}: EnhancedRouteProps) => {
  let { layout: Layout, content: Content, requiresAuth } = route;

  if (isAuthPending && requiresAuth) {
    return <AppLoader />;
  }

  if (requiresAuth && !isAuthenticated) {
    Layout = authFallbackRoute.layout;
    Content = authFallbackRoute.content;
  }

  return (
    <Layout>
      <Suspense fallback={<AppLoader />}>
        <Content />
      </Suspense>
    </Layout>
  );
};
