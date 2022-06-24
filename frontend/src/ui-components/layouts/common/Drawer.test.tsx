import { createMatchMedia, render, screen, theme } from '../../../tests/utils';
import { Drawer } from './Drawer';

const DRAWER_WIDTH = 240;
const closeDrawer = () => {};

describe('Drawer component', () => {
  it('is permanent', () => {
    window.matchMedia = createMatchMedia(theme.breakpoints.values.lg);

    render(<Drawer onClose={closeDrawer} width={DRAWER_WIDTH} />);

    expect(screen.getByTestId('drawer')).toHaveStyle({ visibility: 'visible' });
  });

  it('is temporary and closed', async () => {
    window.matchMedia = createMatchMedia(theme.breakpoints.values.md);

    render(<Drawer onClose={closeDrawer} width={DRAWER_WIDTH} />);

    expect(screen.getByTestId('drawer')).toHaveStyle({ visibility: 'hidden' });
  });

  it('is temporary and open', async () => {
    window.matchMedia = createMatchMedia(theme.breakpoints.values.md);

    render(<Drawer open onClose={closeDrawer} width={DRAWER_WIDTH} />);

    expect(screen.getByTestId('drawer')).toHaveStyle({ visibility: 'visible' });
  });
});
