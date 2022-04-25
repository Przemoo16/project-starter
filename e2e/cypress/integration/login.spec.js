describe("Login page", () => {
  beforeEach(() => {
    cy.visit("/login");
  });

  it("contains link to the /register route", () => {
    cy.get("[data-testid=registerLink]").should(
      "have.attr",
      "href",
      "/register"
    );
  });

  it("contains link to the /reset-password route", () => {
    cy.get("[data-testid=resetPasswordLink]").should(
      "have.attr",
      "href",
      "/reset-password"
    );
  });

  it("displays invalid email", () => {
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
        cy.get("[data-testid=passwordInput]").type(data.password);

        cy.get("[data-testid=submitButton]").click();

        cy.contains("p", "This field is required");
      });
  });

  it("displays that password is required", () => {
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=emailInput]").type(data.email);

        cy.get("[data-testid=submitButton]").click();

        cy.contains("p", "This field is required");
      });
  });

  it("log in inactive account", () => {
    cy.fixture("../fixtures/inactive-user.json")
      .as("inactiveUserData")
      .then((data) => {
        cy.login(data.email, data.password);

        cy.get("[role=alert]").contains("The account is inactive");
      });
  });

  it("log in with invalid credentials", () => {
    cy.fixture("../fixtures/user.json")
      .as("userData")
      .then((data) => {
        cy.login(data.email, "Invalid password");

        cy.get("[role=alert]").contains("Incorrect email or password");
      });
  });

  it("log in", () => {
    cy.login();

    cy.location("pathname").should("eq", "/dashboard");
  });
});
