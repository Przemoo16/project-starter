import { Account, Config } from '../../backendTypes';

type InvalidTokensListener = () => Promise<void>;

class Backend {
  listenOnInvalidTokens(cb: InvalidTokensListener) {}

  async getCurrentAccount(): Promise<Account> {
    return {
      id: 'testAccountID',
      name: 'Test Account',
    };
  }

  async getConfig(): Promise<Config> {
    return {
      accountNameMinLength: 4,
      accountNameMaxLength: 64,
      accountPasswordMinLength: 8,
      accountPasswordMaxLength: 32,
    };
  }
}

export const backend = new Backend();
