import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { VariantType } from 'notistack';

export interface Notification {
  type: VariantType;
  message: string;
  duration: number;
}

interface UIState {
  notifications: Notification[];
}

const initialState: UIState = {
  notifications: [],
};

const NOTIFICATION_DURATION = 4000;

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

export const notifyInfo = (message: string, duration: number = NOTIFICATION_DURATION) =>
  uiActions.addNotification({ message, type: 'info', duration });
export const notifySuccess = (message: string, duration: number = NOTIFICATION_DURATION) =>
  uiActions.addNotification({ message, type: 'success', duration });
export const notifyError = (message: string, duration: number = NOTIFICATION_DURATION) =>
  uiActions.addNotification({ message, type: 'error', duration });
