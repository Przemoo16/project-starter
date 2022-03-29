import { ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

export const AnonymousLayout = ({ children }: Props) => {
  return <div>{children}</div>;
};
