CREATE TABLE Users (
    ID int,
    UserName char(15) NOT NULL UNIQUE,
    Pass char(14) NOT NULL,
    PRIMARY KEY (ID),
    CHECK (Pass != UserName)
);

CREATE TABLE TextPosts (
    ID int NOT NULL,
    PostID int NOT NULL,
    Title char(36),
    Content char(2500),
    PRIMARY KEY (ID, PostID),
    FOREIGN KEY (ID) REFERENCES Users (ID)
);

CREATE TRIGGER t_enumUsers
AFTER INSERT ON Users
BEGIN
    UPDATE Users
    SET ID = ( SELECT max(ID) + 1 from Users )
    WHERE id = 0;
END;

