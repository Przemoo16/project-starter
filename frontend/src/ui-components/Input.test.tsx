import userEvent from '@testing-library/user-event';
import { useForm } from 'react-hook-form';

import { render, screen, waitFor } from '../tests/utils';
import { PasswordInput } from './Input';

describe('PasswordInput component', () => {
  it('toggles password visibility after clicking the icon', async () => {
    const user = userEvent.setup();
    const Component = () => {
      const { control } = useForm();

      return <PasswordInput name="password" control={control} label="Password" />;
    };
    render(<Component />);

    expect(screen.getByLabelText('Password')).toHaveAttribute('type', 'password');
    expect(screen.getByTestId('visibilityIcon')).toBeInTheDocument();
    expect(screen.queryByTestId('visibilityOffIcon')).not.toBeInTheDocument();

    await user.click(screen.getByLabelText('toggle password visibility'));

    await waitFor(() => expect(screen.getByLabelText('Password')).toHaveAttribute('type', 'text'));
    await screen.findByTestId('visibilityOffIcon');
    await waitFor(() => expect(screen.queryByTestId('visibilityIcon')).not.toBeInTheDocument());

    await user.click(screen.getByLabelText('toggle password visibility'));

    await waitFor(() =>
      expect(screen.getByLabelText('Password')).toHaveAttribute('type', 'password')
    );
    await screen.findByTestId('visibilityIcon');
    await waitFor(() => expect(screen.queryByTestId('visibilityOffIcon')).not.toBeInTheDocument());
  });
});
