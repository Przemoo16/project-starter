import { LoginData, SignUpData, User } from '../backendTypes';
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

  async login(credentials: LoginData) {
    const formData = new FormData();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);
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
    const { data } = await this.client.request('/users/me');
    return data;
  }

  private async refreshTokens(): Promise<void> {
    const {
      data: { accessToken, refreshToken },
    } = await this.client.request('/token/refresh/', {
      method: 'POST',
      data: { refreshToken: this.tokenStorage.refreshToken },
      _skipErrorHandler: true,
    });

    this.setTokens({ accessToken, refreshToken });
  }

  clearCredentials() {
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
}

export const backend = new Backend(process.env.REACT_APP_API_URL || '/api/v1');
