export interface User {
  id: string;
  name: string;
}

export interface SignUpData {
  name: string;
  email: string;
  password: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface ResetPasswordData {
  email: string;
}

export interface SetPasswordData {
  key: string;
  password: string;
}
