import { AxiosError } from 'axios';

import { ErrorResponse } from '../backendTypes';

const UNKNOWN_ERROR: ErrorResponse = {
  case: 'UnknownError',
  detail: 'Unknown error',
  context: null,
};

export const handleError = (error: unknown): ErrorResponse => {
  return (error as AxiosError<ErrorResponse>).response?.data || UNKNOWN_ERROR;
};
