INSERT INTO
    public.user(
        id,
        name,
        email,
        password,
        confirmed_email,
        confirmation_email_key,
        created_at,
        updated_at,
        last_login
    )
VALUES
    (
        '57de5b88-c657-4f66-b445-e45bcceeb32d',
        'Active user',
        'activeUser@email.com',
        '$2b$12$EkoW7QChZ7IlWhvi.BCkQuguYD6MBIV.erOeeSvD5QCUPamjGrRdC',
        TRUE,
        '324b6c77-00a5-45a2-a909-385260da67a0',
        current_timestamp,
        current_timestamp,
        NULL
    ),
    (
        '69426239-4798-4acb-9e7c-8a2b6a8697f4',
        'Inactive user',
        'inactiveUser@email.com',
        '$2b$12$EkoW7QChZ7IlWhvi.BCkQuguYD6MBIV.erOeeSvD5QCUPamjGrRdC',
        FALSE,
        '6d555ddc-6145-4836-9d2b-48693674e286',
        current_timestamp,
        current_timestamp,
        NULL
    );
