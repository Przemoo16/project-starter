describe("Register page", () => {
  beforeEach(() => {
    cy.visit("/register");
  });

  it("contains link to the login page", () => {
    cy.get("[data-testid=loginLink]").should("have.attr", "href", "/login");
  });

  it("displays that name is required", () => {
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=emailInput]").type(data.registerEmail);
        cy.get("[data-testid=passwordInput]").type(data.password);
        cy.get("[data-testid=repeatPasswordInput]").type(data.password);

        cy.get("[data-testid=submitButton]").click();

        cy.get("p").contains("This field is required");
      });
  });

  it("displays that name is too long", () => {
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=nameInput]").type("p".repeat(65));
        cy.get("[data-testid=emailInput]").type(data.registerEmail);
        cy.get("[data-testid=passwordInput]").type(data.password);
        cy.get("[data-testid=repeatPasswordInput]").type(data.password);

        cy.get("[data-testid=submitButton]").click();

        cy.get("p").contains("Name can be up to 64 characters");
      });
  });

  it("displays that email is invalid", () => {
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=nameInput]").type(data.name);
        cy.get("[data-testid=emailInput]").type(data.name);
        cy.get("[data-testid=passwordInput]").type(data.password);
        cy.get("[data-testid=repeatPasswordInput]").type(data.password);

        cy.get("[data-testid=submitButton]").click();

        cy.get("p").contains("Invalid email");
      });
  });

  it("displays that email is required", () => {
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=nameInput]").type(data.name);
        cy.get("[data-testid=passwordInput]").type(data.password);
        cy.get("[data-testid=repeatPasswordInput]").type(data.password);

        cy.get("[data-testid=submitButton]").click();

        cy.get("p").contains("This field is required");
      });
  });

  it("displays that password is required", () => {
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=nameInput]").type(data.name);
        cy.get("[data-testid=emailInput]").type(data.registerEmail);
        cy.get("[data-testid=repeatPasswordInput]").type(data.password);

        cy.get("[data-testid=submitButton]").click();

        cy.get("p").contains("This field is required");
      });
  });

  it("displays that password is too short", () => {
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=nameInput]").type(data.name);
        cy.get("[data-testid=emailInput]").type(data.registerEmail);
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
        cy.get("[data-testid=nameInput]").type(data.name);
        cy.get("[data-testid=emailInput]").type(data.registerEmail);
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
        cy.get("[data-testid=nameInput]").type(data.name);
        cy.get("[data-testid=emailInput]").type(data.registerEmail);
        cy.get("[data-testid=passwordInput]").type(data.password);
        cy.get("[data-testid=repeatPasswordInput]").type(
          `${data.password}-not-match`
        );

        cy.get("[data-testid=submitButton]").click();

        cy.get("p").contains("Password doesn't match");
      });
  });

  it("displays proper message when register with already existing email", () => {
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=nameInput]").type(data.name);
        cy.get("[data-testid=emailInput]").type(data.email);
        cy.get("[data-testid=passwordInput]").type(data.password);
        cy.get("[data-testid=repeatPasswordInput]").type(data.password);

        cy.get("[data-testid=submitButton]").click();

        cy.get("[role=alert]").contains(
          "The account with provided email already exists"
        );
      });
  });

  it("enables to register", () => {
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=nameInput]").type(data.name);
        cy.get("[data-testid=emailInput]").type(data.registerEmail);
        cy.get("[data-testid=passwordInput]").type(data.password);
        cy.get("[data-testid=repeatPasswordInput]").type(data.password);

        cy.get("[data-testid=submitButton]").click();

        cy.get("[role=alert]").contains(
          "Your account has been created. Please check your email and follow the instructions to activate your account"
        );
        cy.location("pathname").should("eq", "/login");
      });
  });

  it("redirects user who is already log in", () => {
    cy.login();
    cy.location("pathname").should("eq", "/dashboard");

    cy.visit("/register");

    cy.location("pathname").should("eq", "/dashboard");
  });
});