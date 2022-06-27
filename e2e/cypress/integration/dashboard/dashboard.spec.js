describe("Dashboard page", () => {
  beforeEach(() => {
    cy.visit("/dashboard");
  });

  it("redirects user who is not log in", () => {
    cy.location("pathname").should("eq", "/login");
  });

  it("can be opened by a logged in user", () => {
    cy.login();

    cy.visit("/dashboard");

    cy.location("pathname").should("eq", "/dashboard");
  });
});
