import {
  Account,
  ChangePasswordData,
  Config,
  ConfirmEmailData,
  LoginData,
  RegisterData,
  ResetPasswordData,
  SetPasswordData,
  UpdateAccountDetailsData,
} from '../backendTypes';
import { RestClient } from './client/restClient';
import { TokenStorage } from './storage/tokenStorage';

type InvalidTokensListener = () => Promise<void>;

class Backend {
  private readonly client: RestClient;
  private readonly tokenStorage = new TokenStorage();
  private invalidTokensListeners: Array<InvalidTokensListener> = [];

  constructor(apiUrl: string) {
    this.client = new RestClient(apiUrl);
    this.client.updateErrorHandles({
      onUnauthorized: () => this.refreshTokens(),
      onInvalidTokens: () => {
        this.clearCredentials();
        return Promise.all(this.invalidTokensListeners.map(cb => cb()));
      },
    });

    const accessToken = this.tokenStorage.accessToken;
    this.client.setAuthHeader(accessToken ? `Bearer ${accessToken}` : null);
  }

  listenOnInvalidTokens(cb: InvalidTokensListener) {
    this.invalidTokensListeners.push(cb);
  }

  async login(data: LoginData) {
    const formData = new FormData();
    formData.append('username', data.email);
    formData.append('password', data.password);
    return this.client
      .request('/token/', {
        method: 'POST',
        data: formData,
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      .then(({ data }) =>
        this.setTokens({ accessToken: data.access_token, refreshToken: data.refresh_token }),
      );
  }

  async register(data: RegisterData) {
    return this.client.request('/users/', {
      method: 'POST',
      data,
    });
  }

  async getCurrentAccount(): Promise<Account> {
    if (!this.tokenStorage.accessToken) {
      throw new Error('No token to get the account');
    }
    const { data } = await this.client.request('/users/me');
    return data;
  }

  async logout() {
    await this.revokeTokens();
    this.clearCredentials();
  }

  private async refreshTokens(): Promise<void> {
    const {
      data: { access_token: accessToken },
    } = await this.client.request('/token/refresh', {
      method: 'POST',
      data: { token: this.tokenStorage.refreshToken },
      _skipErrorHandler: true,
    });

    this.setTokens({ accessToken, refreshToken: this.tokenStorage.refreshToken });
  }

  private async revokeTokens() {
    for (const token of [this.tokenStorage.accessToken, this.tokenStorage.refreshToken]) {
      if (!token) {
        continue;
      }
      try {
        await this.client.request('/token/revoke', {
          method: 'POST',
          data: { token: token },
          _skipErrorHandler: true,
        });
      } catch (e) {
        console.log('Could not revoke token');
      }
    }
  }

  private clearCredentials() {
    this.setTokens({ accessToken: null, refreshToken: null });
  }

  private setTokens({
    accessToken,
    refreshToken,
  }: {
    accessToken: string | null;
    refreshToken: string | null;
  }) {
    this.client.setAuthHeader(accessToken ? `Bearer ${accessToken}` : null);
    this.tokenStorage.accessToken = accessToken;
    this.tokenStorage.refreshToken = refreshToken;
  }

  async confirmEmail(data: ConfirmEmailData) {
    return this.client.request('/users/email-confirmation', {
      method: 'POST',
      data,
    });
  }

  async resetPassword(data: ResetPasswordData) {
    return this.client.request('/users/password/reset', {
      method: 'POST',
      data,
    });
  }

  async setPassword(data: SetPasswordData) {
    return this.client.request('/users/password/set', {
      method: 'POST',
      data,
    });
  }

  async getConfig(): Promise<Config> {
    const { data } = await this.client.request('/config/');
    const {
      userNameMinLength: accountNameMinLength,
      userNameMaxLength: accountNameMaxLength,
      userPasswordMinLength: accountPasswordMinLength,
      userPasswordMaxLength: accountPasswordMaxLength,
      ...rest
    } = data;
    return {
      accountNameMinLength,
      accountNameMaxLength,
      accountPasswordMinLength,
      accountPasswordMaxLength,
      ...rest,
    };
  }

  async updateAccountDetails(data: UpdateAccountDetailsData): Promise<Account> {
    const res = await this.client.request('/users/me', {
      method: 'PATCH',
      data,
    });
    return res.data;
  }

  async changePassword(data: ChangePasswordData) {
    return this.client.request('/users/me/password', {
      method: 'POST',
      data,
    });
  }

  async deleteAccount() {
    return this.client.request('/users/me', {
      method: 'DELETE',
    });
  }
}

export const backend = new Backend(import.meta.env.VITE_API_URL || '/api/v1');
