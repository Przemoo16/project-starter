describe("Login page", () => {
  beforeEach(() => {
    cy.visit("/login");
  });

  it("contains link to the /register page", () => {
    cy.get("[data-testid=registerLink]").should(
      "have.attr",
      "href",
      "/register"
    );
  });

  it("contains link to the /reset-password page", () => {
    cy.get("[data-testid=resetPasswordLink]").should(
      "have.attr",
      "href",
      "/reset-password"
    );
  });

  it("displays that email is invalid", () => {
    cy.fixture("../fixtures/activeUser.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=emailInput]").type(data.name);
        cy.get("[data-testid=passwordInput]").type(data.password);

        cy.get("[data-testid=submitButton]").click();

        cy.get("[id$=helper-text]").should("have.text", "Invalid email");
      });
  });

  it("displays that email is required", () => {
    cy.fixture("../fixtures/activeUser.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=passwordInput]").type(data.password);

        cy.get("[data-testid=submitButton]").click();

        cy.get("[id$=helper-text]").should(
          "have.text",
          "This field is required"
        );
      });
  });

  it("displays that password is required", () => {
    cy.fixture("../fixtures/activeUser.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=emailInput]").type(data.email);

        cy.get("[data-testid=submitButton]").click();

        cy.get("[id$=helper-text]").should(
          "have.text",
          "This field is required"
        );
      });
  });

  it("displays proper message when log in with inactive account", () => {
    cy.fixture("../fixtures/inactiveUser.json")
      .as("userData")
      .then((data) => {
        cy.login(data.email, data.password);

        cy.get("[role=alert]").should(
          "have.text",
          "The account is inactive. Please activate your account to continue"
        );
      });
  });

  it("displays proper message when log in with invalid credentials", () => {
    cy.fixture("../fixtures/activeUser.json")
      .as("userData")
      .then((data) => {
        cy.login(data.email, "Invalid password");

        cy.get("[role=alert]").should(
          "have.text",
          "Incorrect email or password"
        );
      });
  });

  it("enables to log in", () => {
    cy.login();

    cy.location("pathname").should("eq", "/dashboard");
  });

  it("redirects user who is already log in", () => {
    cy.login();
    cy.location("pathname").should("eq", "/dashboard");

    cy.visit("/login");

    cy.location("pathname").should("eq", "/dashboard");
  });
});
