describe("Confirm email page", () => {
  it("contains link to the login page", () => {
    cy.visit("/confirm-email/invalid-key");

    cy.get("[data-testid=loginLink]").should("have.attr", "href", "/login");
  });

  it("shows app loader", () => {
    cy.visit("/confirm-email/invalid-key");

    cy.get("[data-testid=appLoader]").should("exist");
  });

  it("displays proper message when confirm email with invalid key", () => {
    cy.visit("/confirm-email/invalid-key");

    cy.get("[data-testid=appLoader]").should("not.exist");
    cy.get("[data-testid=confirmEmailMessage]").should(
      "have.text",
      "We couldn't confirm your email. Please check if the provided link is correct."
    );
  });

  it("enables to confirm email", () => {
    cy.fixture("../fixtures/inactiveUser.json")
      .as("userData")
      .then((data) => {
        cy.visit(`/confirm-email/${data.confirmationEmailKey}`);
      });

    cy.get("[data-testid=appLoader]").should("not.exist");
    cy.get("[data-testid=confirmEmailMessage]").should(
      "have.text",
      "Your email has been confirmed. You can now log in to your account."
    );
  });
});
