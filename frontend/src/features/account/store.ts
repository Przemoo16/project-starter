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
  updateAccountDetailsErrors: ErrorResponse | null;
  changePasswordPending: boolean;
  changePasswordErrors: ErrorResponse | null;
  deleteAccountPending: boolean;
  deleteAccountErrors: ErrorResponse | null;
  deleteAccountModalOpen: boolean;
}

const initialState: AccountState = {
  updateAccountDetailsPending: false,
  updateAccountDetailsErrors: null,
  changePasswordPending: false,
  changePasswordErrors: null,
  deleteAccountPending: false,
  deleteAccountErrors: null,
  deleteAccountModalOpen: false,
};

export const accountSlice = createSlice({
  name: 'account',
  initialState,
  reducers: {
    updateAccountDetails(state, action: PayloadAction<UpdateAccountDetailsData>) {
      state.updateAccountDetailsPending = true;
      state.updateAccountDetailsErrors = null;
    },
    updateAccountDetailsSuccess(state) {
      state.updateAccountDetailsPending = false;
      state.updateAccountDetailsErrors = null;
    },
    updateAccountDetailsFailure(state, { payload }: PayloadAction<{ errors: ErrorResponse }>) {
      state.updateAccountDetailsPending = false;
      state.updateAccountDetailsErrors = payload.errors;
    },
    changePassword(state, action: PayloadAction<ChangePasswordData>) {
      state.changePasswordPending = true;
      state.changePasswordErrors = null;
    },
    changePasswordSuccess(state) {
      state.changePasswordPending = false;
      state.changePasswordErrors = null;
    },
    changePasswordFailure(state, { payload }: PayloadAction<{ errors: ErrorResponse }>) {
      state.changePasswordPending = false;
      state.changePasswordErrors = payload.errors;
    },
    deleteAccount(state, action: PayloadAction<LoginData>) {
      state.deleteAccountPending = true;
      state.deleteAccountErrors = null;
    },
    deleteAccountSuccess(state) {
      state.deleteAccountPending = false;
      state.deleteAccountErrors = null;
    },
    deleteAccountFailure(state, { payload }: PayloadAction<{ errors: ErrorResponse }>) {
      state.deleteAccountPending = false;
      state.deleteAccountErrors = payload.errors;
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
