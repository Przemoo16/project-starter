export class TokenStorage {
  get accessToken() {
    return localStorage.getItem('auth:accessToken');
  }

  set accessToken(token) {
    if (token) {
      localStorage.setItem('auth:accessToken', token);
    } else {
      localStorage.removeItem('auth:accessToken');
    }
  }

  get refreshToken() {
    return localStorage.getItem('auth:refreshToken');
  }

  set refreshToken(token) {
    if (token) {
      localStorage.setItem('auth:refreshToken', token);
    } else {
      localStorage.removeItem('auth:refreshToken');
    }
  }
}
