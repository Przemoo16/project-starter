describe("Logout functionality", () => {
  beforeEach(() => {
    cy.login();
  });

  it("enables to log out", () => {
    cy.get("[data-testid=accountButton]").click();
    cy.get("[data-testid=logoutItem]").click();

    cy.location("pathname").should("eq", "/login");
  });

  it("provides user cannot access protected page after logout", () => {
    cy.get("[data-testid=accountButton]").click();
    cy.get("[data-testid=logoutItem]").click();
    cy.location("pathname").should("eq", "/login");

    cy.visit("/dashboard");

    cy.location("pathname").should("eq", "/login");
  });
});
