describe("404 page", () => {
  beforeEach(() => {
    cy.visit("/invalid-page");
  });

  it("contains button with link to the /login page", () => {
    cy.get("[data-testid=loginButton]").should("have.attr", "href", "/login");
  });
});
