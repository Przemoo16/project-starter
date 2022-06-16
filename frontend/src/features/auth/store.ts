import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { AxiosError } from 'axios';
import { channel } from 'redux-saga';
import { fork, put, takeEvery, takeLeading } from 'redux-saga/effects';

import {
  ConfirmEmailData,
  LoginData,
  RegisterData,
  ResetPasswordData,
  SetPasswordData,
  User,
} from '../../backendTypes';
import { t } from '../../i18n';
import { backend } from '../../services/backend';
import { history } from '../../services/history';
import { notifyError, notifySuccess } from '../../ui-components/store';

interface AuthState {
  user: User | null;
  requestPending: boolean;
  requestSuccess: boolean;
}

const initialState: AuthState = {
  user: null,
  requestPending: true,
  requestSuccess: false,
};

export const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    loadUser(state, { payload }: PayloadAction<{ user: User | null }>) {
      state.requestPending = false;
      state.requestSuccess = false;
      state.user = payload.user;
    },
    login(state, action: PayloadAction<LoginData>) {
      state.requestPending = true;
      state.requestSuccess = false;
    },
    loginSuccess(state, { payload }: PayloadAction<{ user: User }>) {
      state.requestPending = false;
      state.requestSuccess = true;
      state.user = payload.user;
    },
    loginFailure(state) {
      state.requestPending = false;
      state.requestSuccess = false;
      state.user = null;
    },
    register(state, action: PayloadAction<RegisterData>) {
      state.requestPending = true;
      state.requestSuccess = false;
    },
    registerSuccess(state) {
      state.requestPending = false;
      state.requestSuccess = true;
    },
    registerFailure(state) {
      state.requestPending = false;
      state.requestSuccess = false;
    },
    logout(state) {
      state.user = null;
    },
    resetPassword(state, action: PayloadAction<ResetPasswordData>) {
      state.requestPending = true;
      state.requestSuccess = false;
    },
    resetPasswordSuccess(state) {
      state.requestPending = false;
      state.requestSuccess = true;
    },
    resetPasswordFailure(state) {
      state.requestPending = false;
      state.requestSuccess = false;
    },
    setPassword(state, action: PayloadAction<SetPasswordData>) {
      state.requestPending = true;
      state.requestSuccess = false;
    },
    setPasswordSuccess(state) {
      state.requestPending = false;
      state.requestSuccess = true;
    },
    setPasswordFailure(state) {
      state.requestPending = false;
      state.requestSuccess = false;
    },
    confirmEmail(state, action: PayloadAction<ConfirmEmailData>) {
      state.requestPending = true;
      state.requestSuccess = false;
    },
    confirmEmailSuccess(state) {
      state.requestPending = false;
      state.requestSuccess = true;
    },
    confirmEmailFailure(state) {
      state.requestPending = false;
      state.requestSuccess = false;
    },
  },
});

export const authActions = authSlice.actions;

function* loginSaga() {
  try {
    const { ...data } = yield backend.getCurrentUser();
    yield put(authActions.loadUser({ user: data }));
  } catch {
    yield put(authActions.loadUser({ user: null }));
  }

  yield takeLeading(authActions.login, function* ({ payload }) {
    try {
      yield backend.login(payload);
      const { ...data } = yield backend.getCurrentUser();
      yield put(authActions.loginSuccess({ user: data }));
      history.push('/dashboard');
    } catch (e) {
      const error = e as AxiosError;
      if (error.response?.status === 403) {
        yield put(notifyError(t('auth.inactiveAccount')));
      } else {
        yield put(notifyError(t('auth.loginError')));
      }
      yield put(authActions.loginFailure());
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
      const error = e as AxiosError;
      if (error.response?.status === 409) {
        yield put(notifyError(t('auth.accountAlreadyExists')));
      } else {
        yield put(notifyError(t('auth.registerError')));
      }
      yield put(authActions.registerFailure());
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
      yield put(authActions.resetPasswordFailure());
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
      yield put(authActions.setPasswordFailure());
    }
  });
}

function* confirmEmailSaga() {
  yield takeLeading(authActions.confirmEmail, function* ({ payload }) {
    try {
      yield backend.confirmEmail(payload);
      yield put(authActions.confirmEmailSuccess());
    } catch (e) {
      yield put(authActions.confirmEmailFailure());
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
