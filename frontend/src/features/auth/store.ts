import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { channel } from 'redux-saga';
import { fork, put, takeEvery, takeLeading } from 'redux-saga/effects';

import { LoginData, User } from '../../backendTypes';
import { t } from '../../i18n';
import { backend } from '../../services/backend';
import { history } from '../../services/history';
import { notifyError } from '../../ui-components/store';

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
    logout(state) {
      state.user = null;
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
      yield put(history.push('/authenticated') as any);
    } catch (e) {
      yield put(authActions.loginFailure());
      yield put(notifyError(t('auth.loginError')));
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

export function* authSaga() {
  yield fork(loginSaga);
  yield fork(logoutSaga);
}
