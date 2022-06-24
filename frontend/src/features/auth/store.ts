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

interface AuthState {
  account: Account | null;
  pending: boolean;
  errors: ErrorResponse | null;
}

const initialState: AuthState = {
  account: null,
  pending: true,
  errors: null,
};

export const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    loadAccount(state, { payload }: PayloadAction<{ account: Account | null }>) {
      state.pending = false;
      state.errors = null;
      state.account = payload.account;
    },
    login(state, action: PayloadAction<LoginData>) {
      state.pending = true;
      state.errors = null;
    },
    loginSuccess(state, { payload }: PayloadAction<{ account: Account }>) {
      state.pending = false;
      state.errors = null;
      state.account = payload.account;
    },
    loginFailure(state, { payload }: PayloadAction<{ errors: ErrorResponse }>) {
      state.pending = false;
      state.errors = payload.errors;
      state.account = null;
    },
    register(state, action: PayloadAction<RegisterData>) {
      state.pending = true;
      state.errors = null;
    },
    registerSuccess(state) {
      state.pending = false;
      state.errors = null;
    },
    registerFailure(state, { payload }: PayloadAction<{ errors: ErrorResponse }>) {
      state.pending = false;
      state.errors = payload.errors;
    },
    logout(state) {
      state.account = null;
    },
    resetPassword(state, action: PayloadAction<ResetPasswordData>) {
      state.pending = true;
      state.errors = null;
    },
    resetPasswordSuccess(state) {
      state.pending = false;
      state.errors = null;
    },
    resetPasswordFailure(state, { payload }: PayloadAction<{ errors: ErrorResponse }>) {
      state.pending = false;
      state.errors = payload.errors;
    },
    setPassword(state, action: PayloadAction<SetPasswordData>) {
      state.pending = true;
      state.errors = null;
    },
    setPasswordSuccess(state) {
      state.pending = false;
      state.errors = null;
    },
    setPasswordFailure(state, { payload }: PayloadAction<{ errors: ErrorResponse }>) {
      state.pending = false;
      state.errors = payload.errors;
    },
    confirmEmail(state, action: PayloadAction<ConfirmEmailData>) {
      state.pending = true;
      state.errors = null;
    },
    confirmEmailSuccess(state) {
      state.pending = false;
      state.errors = null;
    },
    confirmEmailFailure(state, { payload }: PayloadAction<{ errors: ErrorResponse }>) {
      state.pending = false;
      state.errors = payload.errors;
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
  const badTokenChannel = channel<any>();
  backend.listenOnInvalidTokens(async () => badTokenChannel.put(''));
  yield takeEvery(badTokenChannel, function* () {
    yield put(authActions.logout());
  });

  yield takeLeading(authActions.logout, function* () {
    yield backend.logout();
    window.location.assign('/');
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
      yield put(notifyError(t('auth.setPasswordError')));
      yield put(authActions.setPasswordFailure({ errors: handleError(e) }));
    }
  });
}

function* confirmEmailSaga() {
  yield takeLeading(authActions.confirmEmail, function* ({ payload }) {
    try {
      yield backend.confirmEmail(payload);
      yield put(authActions.confirmEmailSuccess());
    } catch (e) {
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
