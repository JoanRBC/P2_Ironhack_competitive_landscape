CREATE TABLE schools (
    website VARCHAR(64),
    description VARCHAR(1000),
    school VARCHAR(64),
    school_id INT NOT NULL,
    PRIMARY KEY(school_id)
);

CREATE TABLE badges (
    name VARCHAR(64),
    keyword VARCHAR(255),
    description VARCHAR(1000),
    school_id INT NOT NULL,
    PRIMARY KEY(school_id)
);