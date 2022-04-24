import { ThemeProvider } from '@mui/material/styles';
import { render, RenderOptions } from '@testing-library/react';
import mediaQuery from 'css-mediaquery';
import { ReactElement, ReactNode } from 'react';
import { Provider as ReduxProvider } from 'react-redux';
import { MemoryRouter } from 'react-router-dom';

import { createStore } from '../services/store';
import { theme } from '../ui-components/theme';

interface WrapperProps {
  children: ReactNode;
}

const customRender = (ui: ReactElement, options?: Omit<RenderOptions, 'wrapper'>) => {
  const Wrapper = ({ children }: WrapperProps) => {
    return (
      <ReduxProvider store={createStore()}>
        <ThemeProvider theme={theme}>
          <MemoryRouter>{children}</MemoryRouter>
        </ThemeProvider>
      </ReduxProvider>
    );
  };

  return render(ui, { wrapper: Wrapper, ...options });
};

export * from '@testing-library/react';
export { customRender as render };
export { theme };

export const createMatchMedia = (width: number) => (query: string) => ({
  matches: mediaQuery.match(query, {
    width,
  }),
  media: query,
  onchange: null,
  addListener: () => {},
  removeListener: () => {},
  addEventListener: () => {},
  removeEventListener: () => {},
  dispatchEvent: () => true,
});
