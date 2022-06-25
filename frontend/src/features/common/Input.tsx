import {
  PasswordInput as BasePasswordInput,
  PasswordInputProps as BasePasswordInputProps,
  TextInput as BaseTextInput,
  TextInputProps as BaseTextInputProps,
} from '../../ui-components/Input';

type CommonFields = 'size' | 'margin' | 'fullWidth';
type TextInputProps = Omit<BaseTextInputProps, CommonFields>;
type PasswordInputProps = Omit<BasePasswordInputProps, CommonFields>;

export const TextInput = (props: TextInputProps) => (
  <BaseTextInput size="small" margin="normal" fullWidth {...props} />
);

export const PasswordInput = (props: PasswordInputProps) => (
  <BasePasswordInput size="small" margin="normal" fullWidth {...props} />
);
