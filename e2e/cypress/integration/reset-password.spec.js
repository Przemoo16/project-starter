describe("Reset password page", () => {
  beforeEach(() => {
    cy.visit("/reset-password");
  });

  it("contains link to the login page", () => {
    cy.get("[data-testid=loginLink]").should("have.attr", "href", "/login");
  });

  it("displays that email is invalid", () => {
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=emailInput]").type(data.name);

        cy.get("[data-testid=submitButton]").click();

        cy.contains("p", "Invalid email");
      });
  });

  it("displays that email is required", () => {
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=submitButton]").click();

        cy.contains("p", "This field is required");
      });
  });

  it("enables to reset password", () => {
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=emailInput]").type(data.email);

        cy.get("[data-testid=submitButton]").click();

        cy.get("[role=alert]").contains(
          "We've sent you an e-mail with instructions on how to reset your password"
        );
        cy.location("pathname").should("eq", "/login");
      });
  });

  it("redirects user who is already log in", () => {
    cy.login();
    cy.location("pathname").should("eq", "/dashboard");

    cy.visit("/reset-password");

    cy.location("pathname").should("eq", "/dashboard");
  });
});
