import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { AxiosError } from 'axios';
import { channel } from 'redux-saga';
import { fork, put, takeEvery, takeLeading } from 'redux-saga/effects';

import {
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
  pending: boolean;
}

const initialState: AuthState = {
  user: null,
  pending: true,
};

export const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    loadUser(state, { payload }: PayloadAction<{ user: User | null }>) {
      state.pending = false;
      state.user = payload.user;
    },
    login(state, action: PayloadAction<LoginData>) {
      state.pending = true;
    },
    loginSuccess(state, { payload }: PayloadAction<{ user: User }>) {
      state.pending = false;
      state.user = payload.user;
    },
    loginFailure(state) {
      state.pending = false;
      state.user = null;
    },
    register(state, action: PayloadAction<RegisterData>) {},
    logout(state) {
      state.user = null;
    },
    resetPassword(state, action: PayloadAction<ResetPasswordData>) {},
    setPassword(state, action: PayloadAction<SetPasswordData>) {},
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
      history.push('/authenticated');
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
      history.push('/login');
    } catch (e) {
      const error = e as AxiosError;
      if (error.response?.status === 409) {
        yield put(notifyError(t('auth.accountAlreadyExists')));
      } else {
        yield put(notifyError(t('auth.registerError')));
      }
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
      history.push('/login');
    } catch (e) {
      yield put(notifyError(t('auth.resetPasswordError')));
    }
  });
}

function* setPasswordSaga() {
  yield takeLeading(authActions.setPassword, function* ({ payload }) {
    try {
      yield backend.setPassword(payload);
      yield put(notifySuccess(t('auth.setPasswordSuccess')));
      history.push('/login');
    } catch (e) {
      yield put(notifyError(t('auth.setPasswordError')));
    }
  });
}

export function* authSaga() {
  yield fork(loginSaga);
  yield fork(registerSaga);
  yield fork(logoutSaga);
  yield fork(resetPasswordSaga);
  yield fork(setPasswordSaga);
}
