import userEvent from '@testing-library/user-event';
import { useDispatch } from 'react-redux';

import { render, screen, waitFor } from '../tests/utils';
import { Snackbar, SnackbarProvider } from './Snackbar';
import { uiActions } from './store';

const Component = () => {
  const dispatch = useDispatch();
  const { addNotification } = uiActions;

  const handleClick = () => {
    dispatch(addNotification({ message: 'Test message', type: 'error', duration: 4000 }));
  };
  return (
    <button data-testid="snackbar-button" onClick={handleClick}>
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
      </SnackbarProvider>
    );

    const button = screen.getByTestId('snackbar-button');
    await user.click(button);
    await user.click(button);
    await user.click(button);

    expect(screen.getAllByRole('alert').length).toBe(maxSnacks);
  });

  it('closes after clicking the close button', async () => {
    const user = userEvent.setup();
    render(
      <SnackbarProvider maxSnacks={2}>
        <Component />
        <Snackbar />
      </SnackbarProvider>
    );

    await user.click(screen.getByTestId('snackbar-button'));

    expect(screen.getByRole('alert')).toBeInTheDocument();

    await user.click(screen.getByLabelText('close'));

    await waitFor(() => expect(screen.queryByRole('alert')).not.toBeInTheDocument());
  });
});
