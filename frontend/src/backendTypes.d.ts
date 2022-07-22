interface JsonArray extends Array<AnyJson> {}
type AnyJson = boolean | number | string | null | JsonArray | JsonMap;
interface JsonMap {
  [key: string]: AnyJson;
}

export interface ErrorResponse {
  case: string;
  detail: string;
  context: JsonMap | JsonMap[] | null;
}

export interface Account {
  id: string;
  email: string;
  name: string;
  avatar?: string;
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
  token: string;
}

export interface ResetPasswordData {
  email: string;
}

export interface SetPasswordData {
  token: string;
  password: string;
}

export interface Config {
  accountNameMinLength: number;
  accountNameMaxLength: number;
  accountPasswordMinLength: number;
  accountPasswordMaxLength: number;
}

export interface UpdateAccountDetailsData {
  name: string;
}

export interface ChangePasswordData {
  currentPassword: string;
  newPassword: string;
}
