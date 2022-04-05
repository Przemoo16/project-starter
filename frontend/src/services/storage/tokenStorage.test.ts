import { TokenStorage } from './tokenStorage';

describe('Token Storage', () => {
  it('sets access token', () => {
    const token = 'TestToken';
    const storage = new TokenStorage();

    storage.accessToken = token;

    expect(localStorage.getItem('auth:accessToken')).toBe(token);
  });

  it('removes access token', () => {
    localStorage.setItem('auth:accessToken', 'TestToken');
    const storage = new TokenStorage();

    storage.accessToken = null;

    expect(localStorage.getItem('auth:accessToken')).toBe(null);
  });

  it('gets access token', () => {
    const token = 'TestToken';
    const storage = new TokenStorage();

    localStorage.setItem('auth:accessToken', token);

    expect(storage.accessToken).toBe(token);
  });

  it('sets refresh token', () => {
    const token = 'TestToken';
    const storage = new TokenStorage();

    storage.refreshToken = token;

    expect(localStorage.getItem('auth:refreshToken')).toBe(token);
  });

  it('removes refresh token', () => {
    localStorage.setItem('auth:refreshToken', 'TestToken');
    const storage = new TokenStorage();

    storage.refreshToken = null;

    expect(localStorage.getItem('auth:refreshToken')).toBe(null);
  });

  it('gets refresh token', () => {
    const token = 'TestToken';
    const storage = new TokenStorage();

    localStorage.setItem('auth:refreshToken', token);

    expect(storage.refreshToken).toBe(token);
  });
});
