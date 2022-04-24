import userEvent from '@testing-library/user-event';

import { createMatchMedia, render, screen, theme } from '../../tests/utils';
import { DashboardLayout } from './DashboardLayout';

describe('DashboardLayout component', () => {
  it('displays permanent drawer', () => {
    window.matchMedia = createMatchMedia(theme.breakpoints.values.lg);
    render(<DashboardLayout>Content</DashboardLayout>);

    expect(screen.getByTestId('drawer')).toHaveStyle({ visibility: 'visible' });
  });

  it('displays temporary drawer and toggles it when clicking the menu icon', async () => {
    const user = userEvent.setup();
    window.matchMedia = createMatchMedia(theme.breakpoints.values.md);
    render(<DashboardLayout>Content</DashboardLayout>);

    expect(screen.getByTestId('drawer')).toHaveStyle({ visibility: 'hidden' });

    await user.click(screen.getByLabelText('open menu'));

    expect(screen.getByTestId('drawer')).toHaveStyle({ visibility: 'visible' });
  });
});
