import './index.css';

import { Route, Routes } from 'react-router-dom';

import { LazyPages } from './pages/lazy';
import { AnonymousLayout } from './ui-components/layouts/AnonymousLayout';
import { AuthLayout } from './ui-components/layouts/AuthLayout';
import { EnhancedRoute, RouteDefinition } from './ui-components/Routing';

const route404: RouteDefinition = {
  path: '*',
  requiresAuth: false,
  layout: AnonymousLayout,
  content: () => <>404</>,
};

const routes: RouteDefinition[] = [
  { path: '/', requiresAuth: false, layout: AnonymousLayout, content: LazyPages.HomePage },
  {
    path: '/login',
    requiresAuth: false,
    layout: AuthLayout,
    content: LazyPages.LoginPage,
  },
  route404,
];

const App = () => {
  // TODO: Implement authentication
  const isAuthenticated = true;
  const isAuthPending = false;

  return (
    <Routes>
      {routes.map((route, i) => (
        <Route
          key={i}
          path={route.path}
          element={
            <EnhancedRoute
              route={route}
              isAuthenticated={isAuthenticated}
              isAuthPending={isAuthPending}
              authFallbackRoute={route404}
            />
          }
        />
      ))}
    </Routes>
  );
};

export default App;
