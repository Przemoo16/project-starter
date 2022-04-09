import { LoginData, RequestResetPasswordData, SignUpData, User } from '../backendTypes';
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
      .then(({ data }) => this.setTokens(data));
  }

  async signUp(data: SignUpData) {
    return this.client.request('/users/', {
      method: 'POST',
      data,
    });
  }

  async getCurrentUser(): Promise<User> {
    if (!this.tokenStorage.accessToken) {
      throw new Error('No token to get the user with');
    }
    const { data } = await this.client.request('/users/me/');
    return data;
  }

  async logout() {
    await this.revokeTokens();
    this.clearCredentials();
  }

  private async refreshTokens(): Promise<void> {
    const {
      data: { accessToken, refreshToken },
    } = await this.client.request('/token/refresh/', {
      method: 'POST',
      data: { token: this.tokenStorage.refreshToken },
      _skipErrorHandler: true,
    });

    this.setTokens({ accessToken, refreshToken });
  }

  private async revokeTokens() {
    for (const token of [this.tokenStorage.accessToken, this.tokenStorage.refreshToken]) {
      try {
        await this.client.request('/token/revoke/', {
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

  async requestResetPassword(data: RequestResetPasswordData) {
    return this.client.request('/users/password/reset-request/', {
      method: 'POST',
      data,
    });
  }
}

export const backend = new Backend(process.env.REACT_APP_API_URL || '/api/v1');
