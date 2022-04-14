import { render, RenderOptions } from '@testing-library/react';
import { ReactElement, ReactNode } from 'react';
import { Provider as ReduxProvider } from 'react-redux';

import { createStore } from '../services/store';

interface WrapperProps {
  children: ReactNode;
}

const customRender = (ui: ReactElement, options?: Omit<RenderOptions, 'wrapper'>) => {
  const Wrapper = ({ children }: WrapperProps) => {
    return <ReduxProvider store={createStore()}>{children}</ReduxProvider>;
  };

  return render(ui, { wrapper: Wrapper, ...options });
};

export * from '@testing-library/react';
export { customRender as render };
