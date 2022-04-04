import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { useForm } from 'react-hook-form';

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

  it('toggles password visibility after clicking the icon', () => {
    const Component = () => {
      const { control } = useForm();

      return <TextInput name="password" control={control} label="Password" type="password" />;
    };

    render(<Component />);

    expect(screen.getByLabelText('Password')).toHaveAttribute('type', 'password');
    expect(screen.getByTestId('VisibilityIcon')).toBeInTheDocument();
    expect(screen.queryByTestId('VisibilityOffIcon')).not.toBeInTheDocument();

    userEvent.click(screen.getByLabelText('toggle password visibility'));

    expect(screen.getByLabelText('Password')).toHaveAttribute('type', 'text');
    expect(screen.getByTestId('VisibilityOffIcon')).toBeInTheDocument();
    expect(screen.queryByTestId('VisibilityIcon')).not.toBeInTheDocument();

    userEvent.click(screen.getByLabelText('toggle password visibility'));

    expect(screen.getByLabelText('Password')).toHaveAttribute('type', 'password');
    expect(screen.getByTestId('VisibilityIcon')).toBeInTheDocument();
    expect(screen.queryByTestId('VisibilityOffIcon')).not.toBeInTheDocument();
  });
});