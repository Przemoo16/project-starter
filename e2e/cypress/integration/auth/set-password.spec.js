describe("Set password page", () => {
  beforeEach(() => {
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.visit(`/set-password/${data.resetPasswordKey}`);
      });
  });

  it("contains link to the login page", () => {
    cy.get("[data-testid=loginLink]").should("have.attr", "href", "/login");
  });

  it("displays that password is required", () => {
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=repeatPasswordInput]").type(data.password);

        cy.get("[data-testid=submitButton]").click();

        cy.get("p").contains("This field is required");
      });
  });

  it("displays that password is too short", () => {
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=passwordInput]").type("p");
        cy.get("[data-testid=repeatPasswordInput]").type(data.password);

        cy.get("[data-testid=submitButton]").click();

        cy.get("p").contains("Password must be at least 8 characters");
      });
  });

  it("displays that password is too long", () => {
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=passwordInput]").type("p".repeat(33));
        cy.get("[data-testid=repeatPasswordInput]").type(data.password);

        cy.get("[data-testid=submitButton]").click();

        cy.get("p").contains("Password can be up to 32 characters");
      });
  });

  it("displays that repeated password does not match", () => {
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=passwordInput]").type(data.password);
        cy.get("[data-testid=repeatPasswordInput]").type(
          `${data.password}-not-match`
        );

        cy.get("[data-testid=submitButton]").click();

        cy.get("p").contains("Password doesn't match");
      });
  });

  it("displays proper message when reset password with invalid key", () => {
    cy.visit("/set-password/invalid-key");
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=passwordInput]").type(data.password);
        cy.get("[data-testid=repeatPasswordInput]").type(data.password);

        cy.get("[data-testid=submitButton]").click();

        cy.get("[role=alert]").contains(
          "We couldn't changed your password. Please check if the provided link is correct"
        );
      });
  });

  it("enables to reset password", () => {
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=passwordInput]").type(data.password);
        cy.get("[data-testid=repeatPasswordInput]").type(data.password);

        cy.get("[data-testid=submitButton]").click();

        cy.get("[role=alert]").contains("Your password has been changed");
        cy.location("pathname").should("eq", "/login");
      });
  });
});
