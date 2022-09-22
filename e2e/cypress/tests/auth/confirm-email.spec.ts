describe("Confirm email page", () => {
  it("contains link to the login page", () => {
    cy.visit("/confirm-email/e19edcd4-1fcb-4e70-86c7-e83c8aec7f06");

    cy.get("[data-testid=loginLink]").should("have.attr", "href", "/login");
  });

  it("shows app loader", () => {
    cy.visit("/confirm-email/e19edcd4-1fcb-4e70-86c7-e83c8aec7f06");

    cy.get("[data-testid=appLoader]").should("exist");
  });

  it("displays proper message when confirm email with invalid token", () => {
    cy.visit("/confirm-email/e19edcd4-1fcb-4e70-86c7-e83c8aec7f06");

    cy.get("[data-testid=appLoader]").should("not.exist");
    cy.get("[data-testid=confirmEmailMessage]").should(
      "have.text",
      "We couldn't confirm your email. Please check if the provided link is correct.",
    );
  });

  it("displays proper message when confirm email with expired token", () => {
    cy.fixture("../fixtures/expiredInactiveUser.json")
      .as("userData")
      .then((data) => {
        cy.visit(`/confirm-email/${data.emailConfirmationToken}`);
      });

    cy.get("[data-testid=appLoader]").should("not.exist");
    cy.get("[data-testid=confirmEmailMessage]").should(
      "have.text",
      "We couldn't confirm your email. Provided link expired.",
    );
  });

  it("displays proper message when confirm already confirmed email", () => {
    cy.fixture("../fixtures/activeUser.json")
      .as("userData")
      .then((data) => {
        cy.visit(`/confirm-email/${data.emailConfirmationToken}`);
      });

    cy.get("[data-testid=appLoader]").should("not.exist");
    cy.get("[data-testid=confirmEmailMessage]").should(
      "have.text",
      "The email has been already confirmed.",
    );
  });

  it("enables to confirm email", () => {
    cy.fixture("../fixtures/inactiveUser.json")
      .as("userData")
      .then((data) => {
        cy.visit(`/confirm-email/${data.emailConfirmationToken}`);
      });

    cy.get("[data-testid=appLoader]").should("not.exist");
    cy.get("[data-testid=confirmEmailMessage]").should(
      "have.text",
      "Your email has been confirmed. You can now log in to your account.",
    );
  });
});
