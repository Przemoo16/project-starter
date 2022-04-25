import userEvent from '@testing-library/user-event';
import { useForm } from 'react-hook-form';

import { render, screen } from '../tests/utils';
import { TextInput } from './Input';

describe('TextInput component', () => {
  it('is a text type', () => {
    const Component = () => {
      const { control } = useForm();

      return <TextInput name="email" control={control} label="Email" type="text" />;
    };

    render(<Component />);

    expect(screen.getByLabelText('Email')).toHaveAttribute('type', 'text');
    expect(screen.queryByLabelText('toggle password visibility')).not.toBeInTheDocument();
  });

  it('is a password type', () => {
    const Component = () => {
      const { control } = useForm();

      return <TextInput name="password" control={control} label="Password" type="password" />;
    };

    render(<Component />);

    expect(screen.getByLabelText('Password')).toHaveAttribute('type', 'password');
    expect(screen.getByLabelText('toggle password visibility')).toBeInTheDocument();
  });

  it('toggles password visibility after clicking the icon', async () => {
    const user = userEvent.setup();
    const Component = () => {
      const { control } = useForm();

      return <TextInput name="password" control={control} label="Password" type="password" />;
    };
    render(<Component />);

    expect(screen.getByLabelText('Password')).toHaveAttribute('type', 'password');
    expect(screen.getByTestId('visibilityIcon')).toBeInTheDocument();
    expect(screen.queryByTestId('visibilityOffIcon')).not.toBeInTheDocument();

    await user.click(screen.getByLabelText('toggle password visibility'));

    expect(screen.getByLabelText('Password')).toHaveAttribute('type', 'text');
    expect(screen.getByTestId('visibilityOffIcon')).toBeInTheDocument();
    expect(screen.queryByTestId('visibilityIcon')).not.toBeInTheDocument();

    await user.click(screen.getByLabelText('toggle password visibility'));

    expect(screen.getByLabelText('Password')).toHaveAttribute('type', 'password');
    expect(screen.getByTestId('visibilityIcon')).toBeInTheDocument();
    expect(screen.queryByTestId('visibilityOffIcon')).not.toBeInTheDocument();
  });
});
