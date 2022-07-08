import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { AxiosError } from 'axios';
import { fork, put, takeLeading } from 'redux-saga/effects';

import {
  ChangePasswordData,
  ErrorResponse,
  LoginData,
  UpdateAccountDetailsData,
} from '../../backendTypes';
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
  deleteAccountModalOpen: boolean;
}

const initialState: AccountState = {
  updateAccountDetailsPending: false,
  changePasswordPending: false,
  deleteAccountPending: false,
  errors: null,
  deleteAccountModalOpen: false,
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
    deleteAccount(state, action: PayloadAction<LoginData>) {
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
    openDeleteAccountModal: state => {
      state.deleteAccountModalOpen = true;
    },
    closeDeleteAccountModal: state => {
      state.deleteAccountModalOpen = false;
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
      const error = e as AxiosError<ErrorResponse>;
      if (error.response?.status === 422) {
        yield put(notifyError(t('account.invalidCurrentPassword')));
      } else {
        yield put(notifyError(t('account.changePasswordError')));
      }
      yield put(accountActions.changePasswordFailure({ errors: handleError(error) }));
    }
  });
}

function* deleteAccountSaga() {
  yield takeLeading(accountActions.deleteAccount, function* ({ payload }) {
    try {
      yield backend.login(payload);
      yield backend.deleteAccount();
      yield put(accountActions.deleteAccountSuccess());
      yield put(authActions.logout());
    } catch (e) {
      const error = e as AxiosError<ErrorResponse>;
      if (error.response?.status === 401) {
        yield put(notifyError(t('account.InvalidPassword')));
      } else {
        yield put(notifyError(t('account.deleteAccountError')));
      }
      yield put(accountActions.deleteAccountFailure({ errors: handleError(error) }));
    }
  });
}

export function* accountSaga() {
  yield fork(updateAccountDetailsSaga);
  yield fork(changePasswordSaga);
  yield fork(deleteAccountSaga);
}
