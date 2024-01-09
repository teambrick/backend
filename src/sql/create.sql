CREATE DATABASE main;
CREATE TABLE Users (
    UserID int NOT NULL,
    HouseholdID int NOT NULL,
    Name varchar(255) NOT NULL,
    PRIMARY KEY (UserID),
    FOREIGN KEY (HouseholdID) REFERENCES Households(HouseholdID),
);
CREATE TABLE Households (
    HouseholdID int NOT NULL,
    NeighbourhoodID int NOT NULL,
    Address varchar(1024) NOT NULL,
    PRIMARY KEY (HouseholdID),
    FOREIGN KEY (NeighbourhoodID) REFERENCES Neighbourhoods(NeighbourhoodID),
);
CREATE TABLE Neighbourhoods (
    NeighbourhoodID int NOT NULL,
    Location varchar(1024) NOT NULL,

    PRIMARY KEY (NeighbourhoodID),
);

CREATE TABLE Users_Recipes (
    UserID int NOT NULL,
    RecipeID int NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (RecipeID) REFERENCES Recipes(RecipeID),
    TimeConsumed int NOT NULL,
    QuantityConsumed int NOT NULL,
)