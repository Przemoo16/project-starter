import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { VariantType } from 'notistack';

export interface Notification {
  type: VariantType;
  message: string;
}

interface UIState {
  notifications: Notification[];
}

const initialState: UIState = {
  notifications: [],
};

export const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    addNotification: (state, action: PayloadAction<Notification>) => {
      state.notifications.push(action.payload);
    },
    clearNotifications: state => {
      state.notifications = [];
    },
  },
});

export const uiActions = uiSlice.actions;

export const notifyInfo = (message: string) =>
  uiSlice.actions.addNotification({ message, type: 'info' });
export const notifySuccess = (message: string) =>
  uiSlice.actions.addNotification({ message, type: 'success' });
export const notifyError = (message: string) =>
  uiSlice.actions.addNotification({ message, type: 'error' });
