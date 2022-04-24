export interface User {
  id: string;
  name: string;
}

export interface RegisterData {
  name: string;
  email: string;
  password: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface ConfirmEmailData {
  key: string;
}

export interface ResetPasswordData {
  email: string;
}

export interface SetPasswordData {
  key: string;
  password: string;
}

export interface Config {
  appName: string;
  userNameMaxLength: number;
  userPasswordMinLength: number;
  userPasswordMaxLength: number;
}
