INSERT
INTO public.user(
    id,
    name,
    email,
    password,
    confirmed_email,
    confirmation_email_key,
    reset_password_key,
    created_at,
    updated_at,
    last_login
    )
VALUES
    (
    '57de5b88-c657-4f66-b445-e45bcceeb32d',
    'Test User',
    'test@email.com',
    '\$2b\$12\$EkoW7QChZ7IlWhvi.BCkQuguYD6MBIV.erOeeSvD5QCUPamjGrRdC',
    TRUE,
    '324b6c77-00a5-45a2-a909-385260da67a0',
    '6ce7ff1d-94bd-49cb-8eef-bf2b69b183a4',
    current_timestamp,
    current_timestamp,
    NULL
    ),
    (
    '69426239-4798-4acb-9e7c-8a2b6a8697f4',
    'Inactive Test User 1',
    'testInactive1@email.com',
    '\$2b\$12\$EkoW7QChZ7IlWhvi.BCkQuguYD6MBIV.erOeeSvD5QCUPamjGrRdC',
    FALSE,
    'c47b1371-53d9-49f6-a8ed-41794cd0d649',
    '22207208-e0c6-4969-9bda-a4adf9ac0525',
    current_timestamp,
    current_timestamp,
    NULL
    ),
    (
    'f3e8d3f0-1014-4418-827e-7c5f31ba1ccd',
    'Inactive Test User 2',
    'testInactive2@email.com',
    '\$2b\$12\$EkoW7QChZ7IlWhvi.BCkQuguYD6MBIV.erOeeSvD5QCUPamjGrRdC',
    FALSE,
    'ad14eba5-80e8-43fa-aebc-86c8ff37e508',
    'a40cfcef-4f56-4801-a2f9-df3bd98a464f',
    current_timestamp,
    current_timestamp,
    NULL
    )
ON CONFLICT DO NOTHING;
