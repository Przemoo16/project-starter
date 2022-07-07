const NEW_PASSWORD = "new-password";

describe("Account page", () => {
  it("redirects user who is not log in", () => {
    cy.visit("/account");

    cy.location("pathname").should("eq", "/login");
  });

  it("can be opened by a logged in user", () => {
    cy.login();

    cy.visit("/account");

    cy.location("pathname").should("eq", "/account");
  });

  it("pre-populates the name field", () => {
    cy.login();

    cy.visit("/account");

    cy.fixture("../fixtures/activeUser.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=nameInput]").should("have.value", data.name);
      });
  });

  it("displays that name is required", () => {
    cy.login();
    cy.visit("/account");
    cy.get("[data-testid=nameInput]").clear();

    cy.get("[data-testid=updateAccountDetailsButton]").click();

    cy.get("[id$=helper-text]").should("have.text", "This field is required");
  });

  it("displays that name is too short", () => {
    cy.login();
    cy.visit("/account");
    cy.get("[data-testid=nameInput]").clear();
    cy.get("[data-testid=nameInput]").type("p");

    cy.get("[data-testid=updateAccountDetailsButton]").click();

    cy.get("[id$=helper-text]").should(
      "have.text",
      "Name must be at least 4 characters"
    );
  });

  it("displays that name is too long", () => {
    cy.login();
    cy.visit("/account");
    cy.get("[data-testid=nameInput]").type("p".repeat(65));

    cy.get("[data-testid=updateAccountDetailsButton]").click();

    cy.get("[id$=helper-text]").should(
      "have.text",
      "Name can be up to 64 characters"
    );
  });

  it("enables to update details", () => {
    cy.login();
    cy.visit("/account");
    cy.get("[data-testid=nameInput]").clear();
    cy.get("[data-testid=nameInput]").type("Updated User Name");

    cy.get("[data-testid=updateAccountDetailsButton]").click();

    cy.get("[role=alert]").should(
      "have.text",
      "Your account details have been updated"
    );
  });

  it("displays empty form to change password", () => {
    cy.login();

    cy.visit("/account");

    cy.get("[data-testid=currentPasswordInput]").should("have.value", "");
    cy.get("[data-testid=newPasswordInput]").should("have.value", "");
    cy.get("[data-testid=repeatNewPasswordInput]").should("have.value", "");
  });

  it("displays that current password is required", () => {
    cy.login();
    cy.visit("/account");
    cy.get("[data-testid=newPasswordInput]").type(NEW_PASSWORD);
    cy.get("[data-testid=repeatNewPasswordInput]").type(NEW_PASSWORD);

    cy.get("[data-testid=changePasswordButton]").click();

    cy.get("[id$=helper-text]").should("have.text", "This field is required");
  });

  it("displays that password is required", () => {
    cy.login();
    cy.visit("/account");
    cy.fixture("../fixtures/activeUser.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=currentPasswordInput]").type(data.password);
      });

    cy.get("[data-testid=changePasswordButton]").click();

    cy.get("[id$=helper-text]").should("have.text", "This field is required");
  });

  it("displays that password is too short", () => {
    cy.login();
    cy.visit("/account");
    cy.fixture("../fixtures/activeUser.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=currentPasswordInput]").type(data.password);
      });
    cy.get("[data-testid=newPasswordInput]").type("p");
    cy.get("[data-testid=repeatNewPasswordInput]").type("p");

    cy.get("[data-testid=changePasswordButton]").click();

    cy.get("[id$=helper-text]").should(
      "have.text",
      "Password must be at least 8 characters"
    );
  });

  it("displays that password is too long", () => {
    cy.login();
    cy.visit("/account");
    cy.fixture("../fixtures/activeUser.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=currentPasswordInput]").type(data.password);
      });
    cy.get("[data-testid=newPasswordInput]").type("p".repeat(33));
    cy.get("[data-testid=repeatNewPasswordInput]").type("p".repeat(33));

    cy.get("[data-testid=changePasswordButton]").click();

    cy.get("[id$=helper-text]").should(
      "have.text",
      "Password can be up to 32 characters"
    );
  });

  it("displays that repeated password does not match", () => {
    cy.login();
    cy.visit("/account");
    cy.fixture("../fixtures/activeUser.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=currentPasswordInput]").type(data.password);
      });
    cy.get("[data-testid=newPasswordInput]").type(NEW_PASSWORD);
    cy.get("[data-testid=repeatNewPasswordInput]").type(
      `${NEW_PASSWORD}-not-match`
    );

    cy.get("[data-testid=changePasswordButton]").click();

    cy.get("[id$=helper-text]").should("have.text", "Password doesn't match");
  });

  it("displays proper message when current password is invalid", () => {
    cy.login();
    cy.visit("/account");
    cy.get("[data-testid=currentPasswordInput]").type("Invalid password");
    cy.get("[data-testid=newPasswordInput]").type(NEW_PASSWORD);
    cy.get("[data-testid=repeatNewPasswordInput]").type(NEW_PASSWORD);

    cy.get("[data-testid=changePasswordButton]").click();

    cy.get("[role=alert]").should("have.text", "Invalid current password");
  });

  it("enables to change password", () => {
    cy.login();
    cy.visit("/account");
    cy.fixture("../fixtures/activeUser.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=currentPasswordInput]").type(data.password);
      });
    cy.get("[data-testid=newPasswordInput]").type(NEW_PASSWORD);
    cy.get("[data-testid=repeatNewPasswordInput]").type(NEW_PASSWORD);

    cy.get("[data-testid=changePasswordButton]").click();

    cy.get("[role=alert]").should(
      "have.text",
      "Your password has been changed"
    );
  });

  it("cleans form after change password", () => {
    cy.login();
    cy.visit("/account");
    cy.fixture("../fixtures/activeUser.json")
      .as("userData")
      .then((data) => {
        cy.get("[data-testid=currentPasswordInput]").type(data.password);
      });
    cy.get("[data-testid=newPasswordInput]").type(NEW_PASSWORD);
    cy.get("[data-testid=repeatNewPasswordInput]").type(NEW_PASSWORD);

    cy.get("[data-testid=changePasswordButton]").click();

    cy.get("[data-testid=currentPasswordInput]").should("have.value", "");
    cy.get("[data-testid=newPasswordInput]").should("have.value", "");
    cy.get("[data-testid=repeatNewPasswordInput]").should("have.value", "");
  });
});
