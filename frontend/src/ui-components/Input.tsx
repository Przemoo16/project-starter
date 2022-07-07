import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import IconButton from '@mui/material/IconButton';
import InputAdornment from '@mui/material/InputAdornment';
import TextField, { TextFieldProps } from '@mui/material/TextField';
import { useState } from 'react';
import { Controller } from 'react-hook-form';

type CommonFields = 'type' | 'error' | 'helperText';

interface InputProps {
  name: string;
  control: any;
  'data-testid'?: string;
}

export type TextInputProps = InputProps & Omit<TextFieldProps, CommonFields>;

export type PasswordInputProps = InputProps &
  Omit<TextFieldProps, 'placeholder' | 'InputProps' | CommonFields>;

export const TextInput = ({
  name,
  control,
  'data-testid': dataTestId,
  ...rest
}: TextInputProps) => (
  <Controller
    name={name}
    control={control}
    render={({ field, fieldState: { error } }) => (
      <TextField
        {...field}
        type="text"
        error={!!error}
        helperText={error?.message}
        inputProps={{ 'data-testid': dataTestId }}
        {...rest}
      />
    )}
  />
);

export const PasswordInput = ({
  name,
  control,
  'data-testid': dataTestId,
  ...rest
}: PasswordInputProps) => {
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
          inputProps={{
            'data-testid': dataTestId,
          }}
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
