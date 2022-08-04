import type { Config } from '@jest/types';

export default async (): Promise<Config.InitialOptions> => {
  return {
    roots: ['<rootDir>/src'],
    collectCoverageFrom: ['src/**/*.{js,jsx,ts,tsx}', '!**/*.d.ts'],
    coveragePathIgnorePatterns: [
      '<rootDir>/src/services/backend.ts',
      '<rootDir>/src/tests/__mocks__/',
      '<rootDir>/src/tests/utils.tsx',
    ],
    moduleNameMapper: {
      '\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$':
        '<rootDir>/src/tests/__mocks__/fileMock.ts',
      '\\.(css|less)$': '<rootDir>/src/tests/__mocks__/styleMock.ts',
    },
    setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],
    testEnvironment: 'jsdom',
    testPathIgnorePatterns: [
      '<rootDir>/node_modules/',
      '<rootDir>/src/tests/__mocks__/',
      '<rootDir>/src/tests/utils.tsx',
    ],
    transform: {
      '^.+\\.(js|jsx|ts|tsx)$': 'babel-jest',
    },
  };
};
