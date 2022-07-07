describe("Set password page", () => {
  beforeEach(() => {
    cy.fixture("../fixtures/activeUser.json")
      .as("userData")
      .then((data) => {
        cy.visit(`/set-password/${data.resetPasswordKey}`);
      });
  });

  it("contains link to the login page", () => {
    cy.get("[data-testid=loginLink]").should("have.attr", "href", "/login");
  });

  it("displays that password is required", () => {
    cy.get("[data-testid=submitButton]").click();

    cy.get("[id$=helper-text]").should("have.text", "This field is required");
  });

  it("displays that password is too short", () => {
    cy.get("[data-testid=passwordInput]").type("p");
    cy.get("[data-testid=repeatPasswordInput]").type("p");

    cy.get("[data-testid=submitButton]").click();

    cy.get("[id$=helper-text]").should(
      "have.text",
      "Password must be at least 8 characters"
    );
  });

  it("displays that password is too long", () => {
    cy.get("[data-testid=passwordInput]").type("p".repeat(33));
    cy.get("[data-testid=repeatPasswordInput]").type("p".repeat(33));

    cy.get("[data-testid=submitButton]").click();

    cy.get("[id$=helper-text]").should(
      "have.text",
      "Password can be up to 32 characters"
    );
  });

  it("displays that repeated password does not match", () => {
    cy.fixture("../fixtures/activeUser.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=passwordInput]").type(data.password);
        cy.get("[data-testid=repeatPasswordInput]").type(
          `${data.password}-not-match`
        );
      });

    cy.get("[data-testid=submitButton]").click();

    cy.get("[id$=helper-text]").should("have.text", "Password doesn't match");
  });

  it("displays proper message when set password with invalid key", () => {
    cy.visit("/set-password/invalid-key");
    cy.fixture("../fixtures/activeUser.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=passwordInput]").type(data.password);
        cy.get("[data-testid=repeatPasswordInput]").type(data.password);
      });

    cy.get("[data-testid=submitButton]").click();

    cy.get("[role=alert]").should(
      "have.text",
      "We couldn't changed your password. Please check if the provided link is correct"
    );
  });

  it("enables to set new password", () => {
    cy.fixture("../fixtures/activeUser.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=passwordInput]").type(data.password);
        cy.get("[data-testid=repeatPasswordInput]").type(data.password);
      });

    cy.get("[data-testid=submitButton]").click();

    cy.get("[role=alert]").should(
      "have.text",
      "Your password has been changed"
    );
    cy.location("pathname").should("eq", "/login");
  });
});
