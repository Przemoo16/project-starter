import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import IconButton from '@mui/material/IconButton';
import InputAdornment from '@mui/material/InputAdornment';
import TextField, { TextFieldProps } from '@mui/material/TextField';
import { useState } from 'react';
import { Controller } from 'react-hook-form';

type CommonFields = 'type' | 'error' | 'helperText';

export type TextInputProps = Omit<TextFieldProps, CommonFields> & {
  name: string;
  control: any;
};

export type PasswordInputProps = Omit<
  TextFieldProps,
  'placeholder' | 'InputProps' | CommonFields
> & {
  name: string;
  control: any;
};

export const TextInput = ({ name, control, ...rest }: TextInputProps) => (
  <Controller
    name={name}
    control={control}
    render={({ field, fieldState: { error } }) => (
      <TextField {...field} type="text" error={!!error} helperText={error?.message} {...rest} />
    )}
  />
);

export const PasswordInput = ({ name, control, ...rest }: PasswordInputProps) => {
  const [passwordVisible, setPasswordVisibility] = useState(false);

  const handlePasswordVisibility = () => {
    setPasswordVisibility(prevState => !prevState);
  };

  return (
    <Controller
      name={name}
      control={control}
      render={({ field, fieldState: { error } }) => (
        <TextField
          {...field}
          type={passwordVisible ? 'text' : 'password'}
          placeholder="********"
          error={!!error}
          helperText={error?.message}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton
                  aria-label="toggle password visibility"
                  onClick={handlePasswordVisibility}
                  edge="end"
                >
                  {passwordVisible ? (
                    <VisibilityOffIcon data-testid="visibilityOffIcon" />
                  ) : (
                    <VisibilityIcon data-testid="visibilityIcon" />
                  )}
                </IconButton>
              </InputAdornment>
            ),
          }}
          {...rest}
        />
      )}
    />
  );
};
