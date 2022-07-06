/// <reference types="cypress" />

import "./commands";
import "./db";

declare global {
  namespace Cypress {
    interface Chainable {
      login(email?: string, password?: string): Chainable<Element>;
    }
  }
}
