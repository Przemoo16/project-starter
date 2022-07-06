describe("Home page", () => {
  it("contains button with link to the /login page", () => {
    cy.visit("/");

    cy.get("[data-testid=loginButton]").should("have.attr", "href", "/login");
  });

  it("redirects user who is already log in", () => {
    cy.login();
    cy.location("pathname").should("eq", "/dashboard");

    cy.visit("/");

    cy.location("pathname").should("eq", "/dashboard");
  });
});
