import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { fork, put, takeLeading } from 'redux-saga/effects';

import { ErrorResponse, UpdateAccountData } from '../../backendTypes';
import { t } from '../../i18n';
import { backend } from '../../services/backend';
import { handleError } from '../../services/utils';
import { notifyError, notifySuccess } from '../../ui-components/store';
import { authActions } from '../auth/store';

interface AccountState {
  pending: boolean;
  errors: ErrorResponse | null;
}

const initialState: AccountState = {
  pending: false,
  errors: null,
};

export const accountSlice = createSlice({
  name: 'account',
  initialState,
  reducers: {
    updateAccount(state, action: PayloadAction<UpdateAccountData>) {
      state.pending = true;
      state.errors = null;
    },
    updateAccountSuccess(state) {
      state.pending = false;
      state.errors = null;
    },
    updateAccountFailure(state, { payload }: PayloadAction<{ errors: ErrorResponse }>) {
      state.pending = false;
      state.errors = payload.errors;
    },
  },
});

export const accountActions = accountSlice.actions;

function* updateAccountSaga() {
  yield takeLeading(accountActions.updateAccount, function* ({ payload }) {
    try {
      const { ...data } = yield backend.updateAccount(payload);
      yield put(authActions.loadAccount({ account: data }));
      yield put(notifySuccess(t('account.updateSuccess')));
      yield put(accountActions.updateAccountSuccess());
    } catch (e) {
      yield put(notifyError(t('account.updateError')));
      yield put(accountActions.updateAccountFailure({ errors: handleError(e) }));
    }
  });
}

export function* accountSaga() {
  yield fork(updateAccountSaga);
}
