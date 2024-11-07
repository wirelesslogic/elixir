CREATE TABLE bolt_users
(
    id                 SERIAL PRIMARY KEY,
    uuid               uuid         NOT NULL DEFAULT gen_random_uuid(),
    name               varchar(100) NOT NULL,
    email              varchar(128) NOT NULL UNIQUE,
    password_hash      varchar(255) NOT NULL,
    is_otp_enabled     bool                  DEFAULT NULL,
    otp_secret         bytea,
    otp_recovery_codes bytea,
    created_on         date         NOT NULL,
    last_login         date         NOT NULL
);

CREATE TABLE bolt_permission_resources
(
    id          SERIAL,
    name        varchar(100) NOT NULL,
    description varchar(255) DEFAULT NULL,

    PRIMARY KEY (id)
);

CREATE TABLE bolt_roles
(
    id          SERIAL,
    name        varchar(100) NOT NULL,
    description varchar(255) DEFAULT NULL,

    PRIMARY KEY (id)
);

CREATE TABLE bolt_permission_actions
(
    id          SERIAL,
    name        varchar(100) NOT NULL,
    description varchar(255) DEFAULT NULL,

    PRIMARY KEY (id)
);

CREATE TABLE bolt_permissions
(
    id          SERIAL,
    name        varchar(100) NOT NULL,
    description varchar(255) DEFAULT NULL,
    resource_id int          NOT NULL,
    action_id   int          NOT NULL,

    PRIMARY KEY (id),

    FOREIGN KEY (resource_id) REFERENCES bolt_permission_resources (id),
    FOREIGN KEY (action_id) REFERENCES bolt_permission_actions (id)
);

CREATE TABLE IF NOT EXISTS bolt_map_roles_permissions
(
    role_id       int NOT NULL,
    permission_id int NOT NULL,

    PRIMARY KEY (role_id, permission_id),

    FOREIGN KEY (role_id) REFERENCES bolt_roles (id),
    FOREIGN KEY (permission_id) REFERENCES bolt_permissions (id)
);

CREATE TABLE bolt_map_users_roles
(
    user_id int NOT NULL,
    role_id int NOT NULL,
    PRIMARY KEY (user_id, role_id),

    FOREIGN KEY (user_id) REFERENCES bolt_users (id),
    FOREIGN KEY (role_id) REFERENCES bolt_roles (id)
);

CREATE TABLE bolt_user_profiles
(
    id      SERIAL PRIMARY KEY,
    user_id int          NOT NULL,
    color   varchar(255) NOT NULL,
    avatar  varchar(255) NOT NULL,

    FOREIGN KEY (user_id) REFERENCES bolt_users (id)
);
