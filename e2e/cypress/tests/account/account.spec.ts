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
    cy.fixture("../fixtures/activeUser.json")
      .as("userData")
      .then((data) => {
        cy.login();

        cy.visit("/account");

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

  it("enables to update the name", () => {
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
});
