import * as Sentry from '@sentry/react';
import { BrowserTracing } from '@sentry/tracing';

export const initSentry = (dsn: string) => {
  try {
    Sentry.init({
      dsn: dsn,
      integrations: [new BrowserTracing()],
      tracesSampleRate: 1.0,
    });
  } catch (e) {
    console.warn(`Could not init Sentry: ${e}`);
  }
};
