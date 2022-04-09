import { configureStore } from '@reduxjs/toolkit';
import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux';
import createSagaMiddleware from 'redux-saga';

import { authSaga, authSlice } from '../features/auth/store';

export const createStore = () => {
  const saga = createSagaMiddleware();

  const store = configureStore({
    reducer: {
      [authSlice.name]: authSlice.reducer,
    },
    middleware: getDefaultMiddleware => getDefaultMiddleware({ thunk: false }).concat(saga),
  });

  saga.run(authSaga);

  return store;
};

type StoreType = ReturnType<typeof createStore>;

export type State = ReturnType<StoreType['getState']>;
export const useAppDispatch = () => useDispatch<StoreType['dispatch']>();
export const useAppSelector: TypedUseSelectorHook<State> = useSelector;
