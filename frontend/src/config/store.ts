import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { fork, put } from 'redux-saga/effects';

import { Config } from '../backendTypes';
import { backend } from '../services/backend';

const initialState: Config = {
  userNameMaxLength: 64,
  userPasswordMinLength: 8,
  userPasswordMaxLength: 32,
};

export const configSlice = createSlice({
  name: 'config',
  initialState,
  reducers: {
    loadConfig: (state, { payload }: PayloadAction<Config>) => {
      state.userNameMaxLength = payload.userNameMaxLength;
      state.userPasswordMinLength = payload.userPasswordMinLength;
      state.userPasswordMaxLength = payload.userPasswordMaxLength;
    },
  },
});

export const configActions = configSlice.actions;

function* loadConfigSaga() {
  const { ...data } = yield backend.getConfig();
  yield put(configActions.loadConfig(data));
}

export function* configSaga() {
  yield fork(loadConfigSaga);
}
