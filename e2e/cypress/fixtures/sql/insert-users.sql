INSERT INTO
    public.user(
        id,
        name,
        email,
        password,
        confirmed_email,
        email_confirmation_token,
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
    ),
    (
        '59bba00f-1e50-48ec-a3e2-fd28918abaa8',
        'Old inactive user',
        'oldInactiveUser@email.com',
        '$2b$12$EkoW7QChZ7IlWhvi.BCkQuguYD6MBIV.erOeeSvD5QCUPamjGrRdC',
        FALSE,
        'e71b6758-aa3a-4fd4-ad8e-daeccee29c6f',
        current_timestamp - (30 || ' days') :: interval,
        current_timestamp - (30 || ' days') :: interval,
        NULL
    );
