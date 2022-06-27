import axios, { AxiosError, AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

import { ErrorResponse } from '../../backendTypes';

const TOKEN_EXPIRED_STATUS_CODE = 422;
const TOKEN_EXPIRED_RESPONSE_CASE = 'JWTDecodeError';
const TOKEN_EXPIRED_RESPONSE_DETAIL = 'Signature has expired';

export interface Callbacks {
  onUnauthorized: () => Promise<unknown>;
  onInvalidTokens: () => Promise<unknown>;
}

interface RequestConfig extends AxiosRequestConfig {
  _skipErrorHandler?: boolean;
}

export class RestClient {
  private readonly fetcher: AxiosInstance;
  private readonly defaultConfig = { method: 'GET' };
  private callbacks: Callbacks = {
    onInvalidTokens: Promise.resolve,
    onUnauthorized: Promise.resolve,
  };

  constructor(apiUrl: string) {
    this.fetcher = axios.create({
      baseURL: apiUrl,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.addErrorHandler();
  }

  private get authHeader() {
    return this.fetcher.defaults.headers.common.Authorization;
  }

  private set authHeader(header) {
    this.fetcher.defaults.headers.common.Authorization = header;
  }

  request(url: string, config: RequestConfig = {}) {
    const conf = stripUndefined({ url, ...this.defaultConfig, ...config }) as AxiosRequestConfig;
    conf.data = config.data instanceof FormData ? config.data : conf.data;
    return this.fetcher(conf);
  }

  setAuthHeader(header: string | null) {
    delete this.fetcher.defaults.headers.common.Authorization;
    if (header) {
      this.authHeader = header;
    }
  }

  updateErrorHandles(callbacks: Callbacks) {
    this.callbacks = callbacks;
  }

  private addErrorHandler() {
    this.fetcher.interceptors.response.use(
      (response: AxiosResponse) => response,
      async (error: AxiosError<ErrorResponse>) => {
        const originalRequest = error.config as RequestConfig;

        if (
          this.authHeader &&
          !originalRequest._skipErrorHandler &&
          error.response?.status === TOKEN_EXPIRED_STATUS_CODE &&
          error.response?.data.case === TOKEN_EXPIRED_RESPONSE_CASE &&
          error.response?.data.detail === TOKEN_EXPIRED_RESPONSE_DETAIL
        ) {
          originalRequest._skipErrorHandler = true;

          try {
            await this.callbacks.onUnauthorized();
          } catch (e) {
            if (this.authHeader) {
              await this.callbacks.onInvalidTokens();
            }
          }

          if (this.authHeader) {
            delete originalRequest.headers?.Authorization;
            return this.fetcher(originalRequest);
          }
        }

        return Promise.reject(error);
      }
    );
  }
}

function stripUndefined<T>(data: T): T {
  return JSON.parse(JSON.stringify(data));
}
