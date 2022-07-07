import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { fork, put } from 'redux-saga/effects';

import { Config } from '../backendTypes';
import { backend } from '../services/backend';

const initialState: Config = {
  accountNameMinLength: 4,
  accountNameMaxLength: 64,
  accountPasswordMinLength: 8,
  accountPasswordMaxLength: 32,
};

export const configSlice = createSlice({
  name: 'config',
  initialState,
  reducers: {
    loadConfig: (state, { payload }: PayloadAction<Config>) => {
      state.accountNameMinLength = payload.accountNameMinLength;
      state.accountNameMaxLength = payload.accountNameMaxLength;
      state.accountPasswordMinLength = payload.accountPasswordMinLength;
      state.accountPasswordMaxLength = payload.accountPasswordMaxLength;
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
