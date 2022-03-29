import { ReactNode } from 'react';
import styled from 'styled-components';

interface Props {
  children: ReactNode;
}

export const AnonymousLayout = ({ children }: Props) => {
  return <Layout>{children}</Layout>;
};

const Layout = styled.div``;
