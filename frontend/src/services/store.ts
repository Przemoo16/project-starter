import { configureStore } from '@reduxjs/toolkit';
import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux';
import createSagaMiddleware from 'redux-saga';

import { configSaga, configSlice } from '../config/store';
import { accountSaga, accountSlice } from '../features/account/store';
import { authSaga, authSlice } from '../features/auth/store';
import { uiSlice } from '../ui-components/store';

export const createStore = () => {
  const saga = createSagaMiddleware();

  const store = configureStore({
    reducer: {
      [authSlice.name]: authSlice.reducer,
      [uiSlice.name]: uiSlice.reducer,
      [configSlice.name]: configSlice.reducer,
      [accountSlice.name]: accountSlice.reducer,
    },
    middleware: getDefaultMiddleware => getDefaultMiddleware({ thunk: false }).concat(saga),
  });

  saga.run(authSaga);
  saga.run(configSaga);
  saga.run(accountSaga);

  return store;
};

type StoreType = ReturnType<typeof createStore>;

export type State = ReturnType<StoreType['getState']>;
export const useAppDispatch = () => useDispatch<StoreType['dispatch']>();
export const useAppSelector: TypedUseSelectorHook<State> = useSelector;
