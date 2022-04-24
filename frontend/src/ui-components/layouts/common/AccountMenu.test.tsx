import userEvent from '@testing-library/user-event';

import { render, screen } from '../../../tests/utils';
import { AccountMenu } from './AccountMenu';

describe('AccountMenu component', () => {
  it('toggles menu when clicking the icon', async () => {
    const user = userEvent.setup();
    render(<AccountMenu />);

    expect(screen.getByTestId('accountMenu')).toHaveStyle({ visibility: 'hidden' });

    await user.click(screen.getByTestId('AccountCircleIcon'));

    expect(screen.getByTestId('accountMenu')).toHaveStyle({ visibility: 'visible' });
  });
});
