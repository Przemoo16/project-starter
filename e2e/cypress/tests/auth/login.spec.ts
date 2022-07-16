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

  it("displays empty form", () => {
    cy.get("[data-testid=emailInput]").should("have.value", "");
    cy.get("[data-testid=passwordInput]").should("have.value", "");
  });

  it("displays that email is invalid", () => {
    cy.fixture("../fixtures/activeUser.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=emailInput]").type(data.name);
        cy.get("[data-testid=passwordInput]").type(data.password);
      });

    cy.get("[data-testid=submitButton]").click();

    cy.get("[id$=helper-text]").should("have.text", "Invalid email");
  });

  it("displays that email is required", () => {
    cy.fixture("../fixtures/activeUser.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=passwordInput]").type(data.password);
      });

    cy.get("[data-testid=submitButton]").click();

    cy.get("[id$=helper-text]").should("have.text", "This field is required");
  });

  it("displays that password is required", () => {
    cy.fixture("../fixtures/activeUser.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=emailInput]").type(data.email);
      });

    cy.get("[data-testid=submitButton]").click();

    cy.get("[id$=helper-text]").should("have.text", "This field is required");
  });

  it("displays proper message when inactive user logs in", () => {
    cy.fixture("../fixtures/inactiveUser.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=emailInput]").type(data.email);
        cy.get("[data-testid=passwordInput]").type(data.password);
      });

    cy.get("[data-testid=submitButton]").click();

    cy.get("[role=alert]").should(
      "have.text",
      "The account is inactive. Please activate your account to proceed"
    );
  });

  it("displays proper message when log in with invalid credentials", () => {
    cy.fixture("../fixtures/activeUser.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=emailInput]").type(data.email);
      });
    cy.get("[data-testid=passwordInput]").type("Invalid password");

    cy.get("[data-testid=submitButton]").click();

    cy.get("[role=alert]").should("have.text", "Incorrect email or password");
  });

  it("enables to log in", () => {
    cy.login();
  });

  it("redirects user who is already log in", () => {
    cy.login();

    cy.visit("/login");

    cy.location("pathname").should("eq", "/dashboard");
  });
});
