import userEvent from '@testing-library/user-event';

import { useAppDispatch } from '../services/store';
import { render, screen, waitFor } from '../tests/utils';
import { Snackbar, SnackbarProvider } from './Snackbar';
import { uiActions } from './store';

const Component = () => {
  const dispatch = useAppDispatch();
  const { addNotification } = uiActions;

  const handleClick = () => {
    const message = `Test message: ${Math.random().toString(16).substring(2, 10)}`;
    dispatch(addNotification({ message: message, type: 'error', duration: 4000 }));
  };
  return (
    <button data-testid="snackbarButton" onClick={handleClick}>
      Test button
    </button>
  );
};

describe('Snackbar component', () => {
  it('displays only certain number of notifications', async () => {
    const user = userEvent.setup();
    const maxSnacks = 2;
    render(
      <SnackbarProvider maxSnacks={maxSnacks}>
        <Component />
        <Snackbar />
      </SnackbarProvider>,
    );

    const button = screen.getByTestId('snackbarButton');
    await user.click(button);
    await user.click(button);
    await user.click(button);

    await waitFor(() => expect(screen.getAllByRole('alert').length).toBe(maxSnacks));
  });

  it('closes after clicking the close button', async () => {
    const user = userEvent.setup();
    render(
      <SnackbarProvider maxSnacks={2}>
        <Component />
        <Snackbar />
      </SnackbarProvider>,
    );

    await user.click(screen.getByTestId('snackbarButton'));

    await screen.findByRole('alert');

    await user.click(screen.getByLabelText('close notification'));

    await waitFor(() => expect(screen.queryByRole('alert')).not.toBeInTheDocument());
  });
});
