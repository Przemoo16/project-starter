import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import IconButton from '@mui/material/IconButton';
import InputAdornment from '@mui/material/InputAdornment';
import TextField, { TextFieldProps } from '@mui/material/TextField';
import { useState } from 'react';
import { Controller } from 'react-hook-form';

type TextInputProps = TextFieldProps & {
  name: string;
  control: any;
};

export const TextInput = ({ name, control, type, ...rest }: TextInputProps) => {
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
          type={passwordVisible ? 'text' : type}
          error={!!error}
          helperText={error?.message}
          InputProps={{
            endAdornment: type === 'password' && (
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
