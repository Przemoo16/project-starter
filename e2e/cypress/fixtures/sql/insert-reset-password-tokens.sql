INSERT INTO
    public.resetpasswordtoken(
        id,
        expire_at,
        created_at,
        updated_at,
        user_id
    )
VALUES
    (
        '6ce7ff1d-94bd-49cb-8eef-bf2b69b183a4',
        current_timestamp + (1 || ' day') :: interval,
        current_timestamp,
        current_timestamp,
        '57de5b88-c657-4f66-b445-e45bcceeb32d'
    ),
    (
        'd0c703d1-839f-424e-8efd-163a05a26466',
        current_timestamp,
        current_timestamp,
        current_timestamp,
        '57de5b88-c657-4f66-b445-e45bcceeb32d'
    ),
    (
        '68e79dff-b5bf-47ed-a94e-7a79f55520a2',
        current_timestamp + (1 || ' day') :: interval,
        current_timestamp,
        current_timestamp,
        '69426239-4798-4acb-9e7c-8a2b6a8697f4'
    );
