describe("404 page", () => {
  it("contains button with link to the /login page", () => {
    cy.visit("/invalid-page");

    cy.get("[data-testid=loginButton]").should("have.attr", "href", "/login");
  });
});
