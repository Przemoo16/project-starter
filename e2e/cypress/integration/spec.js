describe("Sample test", () => {
  it("Checks if cypress runs", () => {
    expect(true).to.equal(true);
  });
});

describe("Sample test 2", () => {
  it("Visits site", () => {
    cy.visit("http://frontend:3000/");
    cy.contains("Project Starter");
  });
});
