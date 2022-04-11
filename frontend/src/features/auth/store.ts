import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { AxiosError } from 'axios';
import { channel } from 'redux-saga';
import { fork, put, takeEvery, takeLeading } from 'redux-saga/effects';

import { LoginData, User } from '../../backendTypes';
import { backend } from '../../services/backend';
import { history } from '../../services/history';

interface AuthState {
  pending: boolean;
  errors?: Record<string, string>;
  user?: User;
}

const initialState: AuthState = {
  pending: true,
};

export const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    loadUser(state, { payload }: PayloadAction<{ user?: User }>) {
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
    loginFailure(state, { payload }: PayloadAction<{ errors: Record<string, string> }>) {
      state.pending = false;
      state.errors = payload.errors;
    },
    logout(state) {
      state.user = undefined;
    },
  },
});

export const authActions = authSlice.actions;

function* loginSaga() {
  try {
    const { user } = yield backend.getCurrentUser();
    yield put(authActions.loadUser({ user }));
  } catch {
    yield put(authActions.loadUser({ user: undefined }));
  }

  yield takeLeading(authActions.login, function* ({ payload }) {
    try {
      yield backend.login(payload);
      const { user } = yield backend.getCurrentUser();
      yield put(authActions.loginSuccess({ user }));
      yield put(history.push('/authenticated') as any);
    } catch (e) {
      const error = e as AxiosError;
      const errors = error.response?.data;
      yield put(authActions.loginFailure({ errors }));
    }
  });
}

export function* logoutSaga() {
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
