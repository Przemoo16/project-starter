import userEvent from '@testing-library/user-event';

import { createMatchMedia, render, screen, theme, waitFor } from '../../tests/utils';
import { DashboardLayout } from './DashboardLayout';

describe('DashboardLayout component', () => {
  it('toggles the drawer', async () => {
    window.matchMedia = createMatchMedia(theme.breakpoints.values.md);
    const user = userEvent.setup();
    render(<DashboardLayout>Content</DashboardLayout>);

    expect(screen.getByTestId('drawer')).toHaveStyle({ visibility: 'hidden' });

    await user.click(screen.getByLabelText('open menu'));

    await waitFor(() =>
      expect(screen.getByTestId('drawer')).toHaveStyle({ visibility: 'visible' }),
    );

    await user.click(screen.getByTestId('navbar'));

    await waitFor(() => expect(screen.getByTestId('drawer')).toHaveStyle({ visibility: 'hidden' }));
  });
});
