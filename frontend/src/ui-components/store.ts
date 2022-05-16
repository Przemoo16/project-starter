import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { VariantType } from 'notistack';

export interface Notification {
  type: VariantType;
  message: string;
  duration: number;
}

interface UIState {
  notifications: Notification[];
  drawerOpen: boolean;
}

const initialState: UIState = {
  notifications: [],
  drawerOpen: false,
};

const NOTIFICATION_DURATION = 4000;

export const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    addNotification: (state, { payload }: PayloadAction<Notification>) => {
      state.notifications.push(payload);
    },
    clearNotifications: state => {
      state.notifications = [];
    },
    openDrawer: state => {
      state.drawerOpen = true;
    },
    closeDrawer: state => {
      state.drawerOpen = false;
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
