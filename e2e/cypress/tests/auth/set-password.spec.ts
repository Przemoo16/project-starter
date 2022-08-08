describe("Set password page", () => {
  beforeEach(() => {
    cy.fixture("../fixtures/activeUser.json")
      .as("userData")
      .then((data) => {
        cy.visit(`/set-password/${data.resetPasswordToken}`);
      });
  });

  it("contains link to the login page", () => {
    cy.get("[data-testid=loginLink]").should("have.attr", "href", "/login");
  });

  it("displays empty form", () => {
    cy.get("[data-testid=passwordInput]").should("have.value", "");
    cy.get("[data-testid=repeatPasswordInput]").should("have.value", "");
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
        cy.get("[data-testid=repeatPasswordInput]").type(`${data.password}@`);
      });

    cy.get("[data-testid=submitButton]").click();

    cy.get("[id$=helper-text]").should("have.text", "Password doesn't match");
  });

  it("displays proper message when set password with invalid token", () => {
    cy.visit("/set-password/e19edcd4-1fcb-4e70-86c7-e83c8aec7f06");
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

  it("displays proper message when inactive user sets password", () => {
    cy.fixture("../fixtures/inactiveUser.json")
      .as("userData")
      .then((data) => {
        cy.visit(`/set-password/${data.resetPasswordToken}`);
        cy.get("[data-testid=passwordInput]").type(data.password);
        cy.get("[data-testid=repeatPasswordInput]").type(data.password);
      });

    cy.get("[data-testid=submitButton]").click();

    cy.get("[role=alert]").should(
      "have.text",
      "The account is inactive. Please activate your account to proceed"
    );
  });

  it("displays proper message when set password with expired token", () => {
    cy.fixture("../fixtures/activeUser.json")
      .as("userData")
      .then((data) => {
        cy.visit(`/set-password/${data.expiredResetPasswordToken}`);
        cy.get("[data-testid=passwordInput]").type(data.password);
        cy.get("[data-testid=repeatPasswordInput]").type(data.password);
      });

    cy.get("[data-testid=submitButton]").click();

    cy.get("[role=alert]").should(
      "have.text",
      "We couldn't changed your password. Provided link expired"
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
