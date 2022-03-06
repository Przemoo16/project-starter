# Project Starter V2

# Rules to follow:

-   All business logic should be put to a dedicated service and not directly to a router,
-   Each additional response, like error, must also be reflected in the router documentation,
-   Use lazy logging,
-   Don't log sensitive information like credentials or keys,
-   Use the following log level structure:
    -   DEBUG: Message for debugging purposes.
        It helps developers to debug the specific process but is not essential in overall operation of the program.
    -   INFO: Message to help other developers understand what happens in overall operation of the program.
    -   WARNING: Something unusual happened, but we handled the case, so it didn't break anything.
        However, special attention should be paid to this,
    -   ERROR: The top-priority issue that breaks the program and has to be investigated.
-   Test coverage score must be kept on the 100% level (don't put `# pragma: no cover` without important reason).
-   Always add annotations and use the most specific types as possible.
