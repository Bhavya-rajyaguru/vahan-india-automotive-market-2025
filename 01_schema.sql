CREATE TABLE vahan (
    month DATE NOT NULL,
    maker VARCHAR(255) COLLATE utf8mb4_bin NOT NULL,
    fuel VARCHAR(100) COLLATE utf8mb4_bin NOT NULL,
    registrations BIGINT NOT NULL CHECK (registrations >= 0),
    source_file VARCHAR(255) NOT NULL,
    PRIMARY KEY (month, maker, fuel)
) DEFAULT CHARACTER SET utf8mb4;
