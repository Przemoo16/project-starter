describe("Register page", () => {
  beforeEach(() => {
    cy.visit("/register");
  });

  it("contains link to the login page", () => {
    cy.get("[data-testid=loginLink]").should("have.attr", "href", "/login");
  });

  it("displays empty form", () => {
    cy.get("[data-testid=nameInput]").should("have.value", "");
    cy.get("[data-testid=emailInput]").should("have.value", "");
    cy.get("[data-testid=passwordInput]").should("have.value", "");
    cy.get("[data-testid=repeatPasswordInput]").should("have.value", "");
  });

  it("displays that name is required", () => {
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=emailInput]").type(data.email);
        cy.get("[data-testid=passwordInput]").type(data.password);
        cy.get("[data-testid=repeatPasswordInput]").type(data.password);
      });

    cy.get("[data-testid=submitButton]").click();

    cy.get("[id$=helper-text]").should("have.text", "This field is required");
  });

  it("displays that name is too short", () => {
    cy.get("[data-testid=nameInput]").type("p");
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=emailInput]").type(data.email);
        cy.get("[data-testid=passwordInput]").type(data.password);
        cy.get("[data-testid=repeatPasswordInput]").type(data.password);
      });

    cy.get("[data-testid=submitButton]").click();

    cy.get("[id$=helper-text]").should(
      "have.text",
      "Name must be at least 4 characters",
    );
  });

  it("displays that name is too long", () => {
    cy.get("[data-testid=nameInput]").type("p".repeat(65));
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=emailInput]").type(data.email);
        cy.get("[data-testid=passwordInput]").type(data.password);
        cy.get("[data-testid=repeatPasswordInput]").type(data.password);
      });

    cy.get("[data-testid=submitButton]").click();

    cy.get("[id$=helper-text]").should(
      "have.text",
      "Name can be up to 64 characters",
    );
  });

  it("displays that email is invalid", () => {
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=nameInput]").type(data.name);
        cy.get("[data-testid=emailInput]").type(data.name);
        cy.get("[data-testid=passwordInput]").type(data.password);
        cy.get("[data-testid=repeatPasswordInput]").type(data.password);
      });

    cy.get("[data-testid=submitButton]").click();

    cy.get("[id$=helper-text]").should("have.text", "Invalid email");
  });

  it("displays that email is required", () => {
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=nameInput]").type(data.name);
        cy.get("[data-testid=passwordInput]").type(data.password);
        cy.get("[data-testid=repeatPasswordInput]").type(data.password);
      });

    cy.get("[data-testid=submitButton]").click();

    cy.get("[id$=helper-text]").should("have.text", "This field is required");
  });

  it("displays that password is required", () => {
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=nameInput]").type(data.name);
        cy.get("[data-testid=emailInput]").type(data.email);
      });

    cy.get("[data-testid=submitButton]").click();

    cy.get("[id$=helper-text]").should("have.text", "This field is required");
  });

  it("displays that password is too short", () => {
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=nameInput]").type(data.name);
        cy.get("[data-testid=emailInput]").type(data.email);
      });
    cy.get("[data-testid=passwordInput]").type("p");
    cy.get("[data-testid=repeatPasswordInput]").type("p");

    cy.get("[data-testid=submitButton]").click();

    cy.get("[id$=helper-text]").should(
      "have.text",
      "Password must be at least 8 characters",
    );
  });

  it("displays that password is too long", () => {
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=nameInput]").type(data.name);
        cy.get("[data-testid=emailInput]").type(data.email);
      });
    cy.get("[data-testid=passwordInput]").type("p".repeat(33));
    cy.get("[data-testid=repeatPasswordInput]").type("p".repeat(33));

    cy.get("[data-testid=submitButton]").click();

    cy.get("[id$=helper-text]").should(
      "have.text",
      "Password can be up to 32 characters",
    );
  });

  it("displays that repeated password does not match", () => {
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=nameInput]").type(data.name);
        cy.get("[data-testid=emailInput]").type(data.email);
        cy.get("[data-testid=passwordInput]").type(data.password);
        cy.get("[data-testid=repeatPasswordInput]").type(`${data.password}@`);
      });

    cy.get("[data-testid=submitButton]").click();

    cy.get("[id$=helper-text]").should("have.text", "Password doesn't match");
  });

  it("displays proper message when register with already existing email", () => {
    cy.fixture("../fixtures/activeUser.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=nameInput]").type(data.name);
        cy.get("[data-testid=emailInput]").type(data.email);
        cy.get("[data-testid=passwordInput]").type(data.password);
        cy.get("[data-testid=repeatPasswordInput]").type(data.password);
      });

    cy.get("[data-testid=submitButton]").click();

    cy.get("[role=alert]").should(
      "have.text",
      "The account with provided email already exists",
    );
  });

  it("enables to register", () => {
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=nameInput]").type(data.name);
        cy.get("[data-testid=emailInput]").type(data.email);
        cy.get("[data-testid=passwordInput]").type(data.password);
        cy.get("[data-testid=repeatPasswordInput]").type(data.password);
      });

    cy.get("[data-testid=submitButton]").click();

    cy.get("[role=alert]").should(
      "have.text",
      "Your account has been created. Please check your email and follow the instructions to activate your account",
    );
    cy.location("pathname").should("eq", "/login");
  });

  it("redirects user who is already log in", () => {
    cy.login();

    cy.visit("/register");

    cy.location("pathname").should("eq", "/dashboard");
  });
});
