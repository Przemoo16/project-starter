import userEvent from '@testing-library/user-event';

import { render, screen, waitFor } from '../../../tests/utils';
import { AccountMenu } from './AccountMenu';

describe('AccountMenu component', () => {
  it('toggles menu when clicking the icon', async () => {
    const user = userEvent.setup();
    render(<AccountMenu />);

    expect(screen.getByTestId('accountMenu')).toHaveStyle({ visibility: 'hidden' });

    await user.click(screen.getByTestId('accountButton'));

    await waitFor(() =>
      expect(screen.getByTestId('accountMenu')).toHaveStyle({ visibility: 'visible' })
    );
  });
});
