import { Config, User } from '../../backendTypes';

type InvalidTokensListener = () => Promise<void>;

class Backend {
  listenOnInvalidTokens(cb: InvalidTokensListener) {}

  async getCurrentUser(): Promise<User> {
    return {
      id: 'testUserID',
      name: 'Test User',
    };
  }

  async getConfig(): Promise<Config> {
    return {
      appName: 'Project Starter',
      userNameMaxLength: 64,
      userPasswordMinLength: 8,
      userPasswordMaxLength: 32,
    };
  }
}

export const backend = new Backend();
