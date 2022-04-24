import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { fork, put } from 'redux-saga/effects';

import { Config } from '../backendTypes';
import { backend } from '../services/backend';

const initialState: Config = {
  appName: 'Project Starter',
  userNameMaxLength: 64,
  userPasswordMinLength: 8,
  userPasswordMaxLength: 32,
};

export const configSlice = createSlice({
  name: 'config',
  initialState,
  reducers: {
    loadConfig: (state, { payload }: PayloadAction<Config>) => {
      state.appName = payload.appName;
      state.userNameMaxLength = payload.userNameMaxLength;
      state.userPasswordMinLength = payload.userPasswordMinLength;
      state.userPasswordMaxLength = payload.userPasswordMaxLength;
    },
  },
});

export const configActions = configSlice.actions;

function* loadConfigSaga() {
  try {
    const { ...data } = yield backend.getConfig();
    yield put(configActions.loadConfig(data));
  } catch (e) {
    console.error('Loading config failed:', e);
  }
}

export function* configSaga() {
  yield fork(loadConfigSaga);
}
