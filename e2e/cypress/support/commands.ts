Cypress.Commands.add("login", (email, password) => {
  cy.visit("/login");
  cy.fixture("../fixtures/activeUser.json")
    .as("userData")
    .then((data) => {
      cy.get("[data-testid=emailInput]").type(email || data.email);
      cy.get("[data-testid=passwordInput]").type(password || data.password);

      cy.get("[data-testid=submitButton]").click();
    });
});
