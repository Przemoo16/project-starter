import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { AxiosError } from 'axios';
import { channel } from 'redux-saga';
import { fork, put, takeEvery, takeLeading } from 'redux-saga/effects';

import {
  Account,
  ConfirmEmailData,
  ErrorResponse,
  LoginData,
  RegisterData,
  ResetPasswordData,
  SetPasswordData,
} from '../../backendTypes';
import { t } from '../../i18n';
import { backend } from '../../services/backend';
import { history } from '../../services/history';
import { handleError } from '../../services/utils';
import { notifyError, notifySuccess } from '../../ui-components/store';

const EMAIL_ALREADY_CONFIRMED_CASE = 'EmailAlreadyConfirmedError';
const EMAIL_CONFIRMATION_TOKEN_EXPIRED_CASE = 'EmailConfirmationTokenExpiredError';
const RESET_PASSWORD_TOKEN_EXPIRED_CASE = 'ResetPasswordTokenExpiredError';

interface AuthState {
  account: Account | null;
  loginPending: boolean;
  loginErrors: ErrorResponse | null;
  registerPending: boolean;
  registerErrors: ErrorResponse | null;
  resetPasswordPending: boolean;
  resetPasswordErrors: ErrorResponse | null;
  setPasswordPending: boolean;
  setPasswordErrors: ErrorResponse | null;
  confirmEmailMessage: string;
  confirmEmailErrors: ErrorResponse | null;
}

const initialState: AuthState = {
  account: null,
  loginPending: true,
  loginErrors: null,
  registerPending: false,
  registerErrors: null,
  resetPasswordPending: false,
  resetPasswordErrors: null,
  setPasswordPending: false,
  setPasswordErrors: null,
  confirmEmailMessage: '',
  confirmEmailErrors: null,
};

export const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    loadAccount(state, { payload }: PayloadAction<{ account: Account | null }>) {
      state.loginPending = false;
      state.loginErrors = null;
      state.account = payload.account;
    },
    login(state, action: PayloadAction<LoginData>) {
      state.loginPending = true;
      state.loginErrors = null;
    },
    loginSuccess(state, { payload }: PayloadAction<{ account: Account }>) {
      state.loginPending = false;
      state.loginErrors = null;
      state.account = payload.account;
    },
    loginFailure(state, { payload }: PayloadAction<{ errors: ErrorResponse }>) {
      state.loginPending = false;
      state.loginErrors = payload.errors;
      state.account = null;
    },
    register(state, action: PayloadAction<RegisterData>) {
      state.registerPending = true;
      state.registerErrors = null;
    },
    registerSuccess(state) {
      state.registerPending = false;
      state.registerErrors = null;
    },
    registerFailure(state, { payload }: PayloadAction<{ errors: ErrorResponse }>) {
      state.registerPending = false;
      state.registerErrors = payload.errors;
    },
    logout(state) {},
    resetPassword(state, action: PayloadAction<ResetPasswordData>) {
      state.resetPasswordPending = true;
      state.resetPasswordErrors = null;
    },
    resetPasswordSuccess(state) {
      state.resetPasswordPending = false;
      state.resetPasswordErrors = null;
    },
    resetPasswordFailure(state, { payload }: PayloadAction<{ errors: ErrorResponse }>) {
      state.resetPasswordPending = false;
      state.resetPasswordErrors = payload.errors;
    },
    setPassword(state, action: PayloadAction<SetPasswordData>) {
      state.setPasswordPending = true;
      state.setPasswordErrors = null;
    },
    setPasswordSuccess(state) {
      state.setPasswordPending = false;
      state.setPasswordErrors = null;
    },
    setPasswordFailure(state, { payload }: PayloadAction<{ errors: ErrorResponse }>) {
      state.setPasswordPending = false;
      state.setPasswordErrors = payload.errors;
    },
    confirmEmail(state, action: PayloadAction<ConfirmEmailData>) {
      state.confirmEmailMessage = '';
      state.confirmEmailErrors = null;
    },
    confirmEmailSuccess(state) {
      state.confirmEmailErrors = null;
    },
    confirmEmailFailure(state, { payload }: PayloadAction<{ errors: ErrorResponse }>) {
      state.confirmEmailErrors = payload.errors;
    },
    setConfirmEmailMessage(state, { payload }: PayloadAction<{ message: string }>) {
      state.confirmEmailMessage = payload.message;
    },
  },
});

export const authActions = authSlice.actions;

function* loginSaga() {
  try {
    const { ...data } = yield backend.getCurrentAccount();
    yield put(authActions.loadAccount({ account: data }));
  } catch {
    yield put(authActions.loadAccount({ account: null }));
  }

  yield takeLeading(authActions.login, function* ({ payload }) {
    try {
      yield backend.login(payload);
      const { ...data } = yield backend.getCurrentAccount();
      yield put(authActions.loginSuccess({ account: data }));
      history.push('/dashboard');
    } catch (e) {
      const error = e as AxiosError<ErrorResponse>;
      if (error.response?.status === 403) {
        yield put(notifyError(t('auth.inactiveAccount')));
      } else {
        yield put(notifyError(t('auth.loginError')));
      }
      yield put(authActions.loginFailure({ errors: handleError(error) }));
    }
  });
}

function* registerSaga() {
  yield takeLeading(authActions.register, function* ({ payload }) {
    try {
      yield backend.register(payload);
      yield put(notifySuccess(t('auth.registerSuccess')));
      yield put(authActions.registerSuccess());
      history.push('/login');
    } catch (e) {
      const error = e as AxiosError<ErrorResponse>;
      if (error.response?.status === 409) {
        yield put(notifyError(t('auth.accountAlreadyExists')));
      } else {
        yield put(notifyError(t('auth.registerError')));
      }
      yield put(authActions.registerFailure({ errors: handleError(error) }));
    }
  });
}

function* logoutSaga() {
  const badTokenChannel = channel<string>();
  backend.listenOnInvalidTokens(async () => badTokenChannel.put(''));
  yield takeEvery(badTokenChannel, function* () {
    yield put(authActions.logout());
  });

  yield takeLeading(authActions.logout, function* () {
    yield backend.logout();
    window.location.assign('/login');
  });
}

function* resetPasswordSaga() {
  yield takeLeading(authActions.resetPassword, function* ({ payload }) {
    try {
      yield backend.resetPassword(payload);
      yield put(notifySuccess(t('auth.resetPasswordSuccess')));
      yield put(authActions.resetPasswordSuccess());
      history.push('/login');
    } catch (e) {
      yield put(notifyError(t('auth.resetPasswordError')));
      yield put(authActions.resetPasswordFailure({ errors: handleError(e) }));
    }
  });
}

function* setPasswordSaga() {
  yield takeLeading(authActions.setPassword, function* ({ payload }) {
    try {
      yield backend.setPassword(payload);
      yield put(notifySuccess(t('auth.setPasswordSuccess')));
      yield put(authActions.setPasswordSuccess());
      history.push('/login');
    } catch (e) {
      const error = e as AxiosError<ErrorResponse>;
      if (error.response?.status === 403) {
        yield put(notifyError(t('auth.inactiveAccount')));
      } else if (
        error.response?.status === 422 &&
        error.response?.data.case === RESET_PASSWORD_TOKEN_EXPIRED_CASE
      ) {
        yield put(notifyError(t('auth.resetPasswordLinkExpired')));
      } else {
        yield put(notifyError(t('auth.setPasswordError')));
      }
      yield put(authActions.setPasswordFailure({ errors: handleError(error) }));
    }
  });
}

function* confirmEmailSaga() {
  yield takeLeading(authActions.confirmEmail, function* ({ payload }) {
    try {
      yield backend.confirmEmail(payload);
      yield put(authActions.confirmEmailSuccess());
      yield put(authActions.setConfirmEmailMessage({ message: t('auth.confirmEmailSuccess') }));
    } catch (e) {
      const error = e as AxiosError<ErrorResponse>;
      if (
        error.response?.status === 422 &&
        error.response?.data.case === EMAIL_ALREADY_CONFIRMED_CASE
      ) {
        yield put(authActions.setConfirmEmailMessage({ message: t('auth.emailAlreadyConfirmed') }));
      } else if (
        error.response?.status === 422 &&
        error.response?.data.case === EMAIL_CONFIRMATION_TOKEN_EXPIRED_CASE
      ) {
        yield put(
          authActions.setConfirmEmailMessage({ message: t('auth.confirmEmailLinkExpired') }),
        );
      } else {
        yield put(authActions.setConfirmEmailMessage({ message: t('auth.confirmEmailError') }));
      }
      yield put(authActions.confirmEmailFailure({ errors: handleError(e) }));
    }
  });
}

export function* authSaga() {
  yield fork(loginSaga);
  yield fork(registerSaga);
  yield fork(logoutSaga);
  yield fork(resetPasswordSaga);
  yield fork(setPasswordSaga);
  yield fork(confirmEmailSaga);
}
