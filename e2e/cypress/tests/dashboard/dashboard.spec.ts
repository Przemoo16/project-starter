describe("Dashboard page", () => {
  it("redirects user who is not log in", () => {
    cy.visit("/dashboard");

    cy.location("pathname").should("eq", "/login");
  });

  it("can be opened by a logged in user", () => {
    cy.login();
  });

  it("enables to go to the account settings", () => {
    cy.login();

    cy.get("[data-testid=accountButton]").click();
    cy.get("[data-testid=accountItem]").click();

    cy.location("pathname").should("eq", "/account");
  });

  it("enables to log out", () => {
    cy.login();

    cy.get("[data-testid=accountButton]").click();
    cy.get("[data-testid=logoutItem]").click();

    cy.location("pathname").should("eq", "/login");
  });

  it("provides user cannot access protected page after logout", () => {
    cy.login();

    cy.get("[data-testid=accountButton]").click();
    cy.get("[data-testid=logoutItem]").click();
    cy.location("pathname").should("eq", "/login");

    cy.visit("/dashboard");

    cy.location("pathname").should("eq", "/login");
  });
});
