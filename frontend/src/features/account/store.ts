import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { fork, put, takeLeading } from 'redux-saga/effects';

import { ChangePasswordData, ErrorResponse, UpdateAccountDetailsData } from '../../backendTypes';
import { t } from '../../i18n';
import { backend } from '../../services/backend';
import { handleError } from '../../services/utils';
import { notifyError, notifySuccess } from '../../ui-components/store';
import { authActions } from '../auth/store';

interface AccountState {
  updateAccountDetailsPending: boolean;
  changePasswordPending: boolean;
  deleteAccountPending: boolean;
  errors: ErrorResponse | null;
}

const initialState: AccountState = {
  updateAccountDetailsPending: false,
  changePasswordPending: false,
  deleteAccountPending: false,
  errors: null,
};

export const accountSlice = createSlice({
  name: 'account',
  initialState,
  reducers: {
    updateAccountDetails(state, action: PayloadAction<UpdateAccountDetailsData>) {
      state.updateAccountDetailsPending = true;
      state.errors = null;
    },
    updateAccountDetailsSuccess(state) {
      state.updateAccountDetailsPending = false;
      state.errors = null;
    },
    updateAccountDetailsFailure(state, { payload }: PayloadAction<{ errors: ErrorResponse }>) {
      state.updateAccountDetailsPending = false;
      state.errors = payload.errors;
    },
    changePassword(state, action: PayloadAction<ChangePasswordData>) {
      state.changePasswordPending = true;
      state.errors = null;
    },
    changePasswordSuccess(state) {
      state.changePasswordPending = false;
      state.errors = null;
    },
    changePasswordFailure(state, { payload }: PayloadAction<{ errors: ErrorResponse }>) {
      state.changePasswordPending = false;
      state.errors = payload.errors;
    },
    deleteAccount(state) {
      state.deleteAccountPending = true;
      state.errors = null;
    },
    deleteAccountSuccess(state) {
      state.deleteAccountPending = false;
      state.errors = null;
    },
    deleteAccountFailure(state, { payload }: PayloadAction<{ errors: ErrorResponse }>) {
      state.deleteAccountPending = false;
      state.errors = payload.errors;
    },
  },
});

export const accountActions = accountSlice.actions;

function* updateAccountDetailsSaga() {
  yield takeLeading(accountActions.updateAccountDetails, function* ({ payload }) {
    try {
      const { ...data } = yield backend.updateAccountDetails(payload);
      yield put(authActions.loadAccount({ account: data }));
      yield put(notifySuccess(t('account.updateAccountDetailsSuccess')));
      yield put(accountActions.updateAccountDetailsSuccess());
    } catch (e) {
      yield put(notifyError(t('account.updateAccountDetailsError')));
      yield put(accountActions.updateAccountDetailsFailure({ errors: handleError(e) }));
    }
  });
}

function* changePasswordSaga() {
  yield takeLeading(accountActions.changePassword, function* ({ payload }) {
    try {
      yield backend.changePassword(payload);
      yield put(notifySuccess(t('account.changePasswordSuccess')));
      yield put(accountActions.changePasswordSuccess());
    } catch (e) {
      yield put(notifyError(t('account.changePasswordError')));
      yield put(accountActions.changePasswordFailure({ errors: handleError(e) }));
    }
  });
}

function* deleteAccountSaga() {
  yield takeLeading(accountActions.deleteAccount, function* () {
    try {
      yield backend.deleteAccount();
      yield put(notifySuccess(t('account.deleteAccountSuccess')));
      yield put(accountActions.deleteAccountSuccess());
    } catch (e) {
      yield put(notifyError(t('account.deleteAccountError')));
      yield put(accountActions.deleteAccountFailure({ errors: handleError(e) }));
    }
  });
}

export function* accountSaga() {
  yield fork(updateAccountDetailsSaga);
  yield fork(changePasswordSaga);
  yield fork(deleteAccountSaga);
}
