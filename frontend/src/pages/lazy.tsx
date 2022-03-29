import { lazy } from 'react';

export const LazyPages = {
  HomePage: lazy(() => import('./home/HomePage')),
};
