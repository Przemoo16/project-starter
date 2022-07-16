import { defineConfig } from "cypress";
import { readFileSync } from "fs";
import { Pool } from "pg";

const TRUNCATE_USER_TABLE_FILE_PATH =
  "./cypress/fixtures/sql/truncate-user-table.sql";
const INSERT_USERS_FILE_PATH = "./cypress/fixtures/sql/insert-users.sql";
const INSERT_RESET_PASSWORD_TOKENS_FILE_PATH =
  "./cypress/fixtures/sql/insert-reset-password-tokens.sql";

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

const truncateUserTable = async () => {
  await pool.query(readFileSync(TRUNCATE_USER_TABLE_FILE_PATH, "utf8"));
};

export default defineConfig({
  e2e: {
    baseUrl: "http://proxy",
    specPattern: "cypress/tests/**/*.spec.{ts,tsx}",
    supportFile: "cypress/support/e2e.ts",
    experimentalSessionAndOrigin: true,

    setupNodeEvents(on, config) {
      on("after:run", async (results) => {
        await truncateUserTable();
        await pool.end();
      });
      on("task", {
        async resetDB() {
          await truncateUserTable();
          await pool.query(readFileSync(INSERT_USERS_FILE_PATH, "utf8"));
          await pool.query(
            readFileSync(INSERT_RESET_PASSWORD_TOKENS_FILE_PATH, "utf8")
          );
          return null;
        },
      });
    },
  },
});
