-- CREATE DATABASE main;

CREATE TABLE Neighbourhoods (
    NeighbourhoodID integer NOT NULL,

    Location varchar(1024) NOT NULL,
    PRIMARY KEY (NeighbourhoodID)
);

CREATE TABLE Households (
    HouseholdID integer NOT NULL,

    NeighbourhoodID integer NOT NULL,

    Address varchar(1024) NOT NULL,
    PRIMARY KEY (HouseholdID)
    FOREIGN KEY (NeighbourhoodID) REFERENCES Neighbourhoods(NeighbourhoodID)
);


CREATE TABLE Users (
    UserID integer NOT NULL,

    HouseholdID integer NOT NULL,

    UserName varchar(256) NOT NULL,
    Password varchar(256) NOT NULL,
    PRIMARY KEY (UserID)
    FOREIGN KEY (HouseholdID) REFERENCES Households(HouseholdID)
);

CREATE TABLE Recipes (
    RecipeID integer NOT NULL,
    RecipeName varchar(256) NOT NULL,
    Description varchar(1024),
    -- There's no result_quantity, we'll just measure calories in Recipes-Nutrients
    Method CLOB, -- just JSON
    PRIMARY KEY (RecipeID)
);

CREATE TABLE Nutrients (
  NutrientID integer NOT NULL,
  NutrientName varchar(128) NOT NULL,
  Data CLOB, -- more JSON
  PRIMARY KEY (NutrientID)
);

CREATE TABLE Ingredients (
  IngredientID integer NOT NULL,
  IngredientName varchar(256) NOT NULL,
  ReadableUnit varchar(32), -- like ml, litre, head of cabbage, kg etc etc
  Data CLOB, -- more JSON for things im not sure
  PRIMARY KEY (IngredientID)
);

CREATE TABLE Users_Recipes (
    UserID integer NOT NULL,

    RecipeID integer NOT NULL,

    TimeConsumed integer NOT NULL,
    QuantityConsumed integer NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
    FOREIGN KEY (RecipeID) REFERENCES Recipes(RecipeID)
);

CREATE TABLE Households_Ingredients (
    HouseholdID integer NOT NULL,

    IngredientID integer NOT NULL,

    Quantity decimal NOT NULL,
    -- both are unix stamps
    BestBefore integer,
    UseBy integer,
    AvailableQuantity decimal,
    FOREIGN KEY (HouseholdID) REFERENCES Households(HouseholdID)
    FOREIGN KEY (IngredientID) REFERENCES Ingredients(IngredientID)
);

CREATE TABLE Recipes_Ingredients (
  RecipeID integer NOT NULL,

  IngredientID integer NOT NULL,

  Quantity decimal NOT NULL,
  -- order to add ingredients, used to reference it in the method
  IngredientIndex integer NOT NULL,
  FOREIGN KEY(RecipeID) REFERENCES Recipes(RecipeID)
  FOREIGN KEY(IngredientID) REFERENCES Ingredients(IngredientID)
);

CREATE TABLE Recipes_Nutrients (
  RecipeID integer NOT NULL,

  NutrientID integer NOT NULL,

  Quantity decimal NOT NULL,
  FOREIGN KEY(RecipeID) REFERENCES Recipes(RecipeID)
  FOREIGN KEY(NutrientID) REFERENCES Nutrients(NutrientID)
);

CREATE TABLE Ingredients_Nutrients (
  IngredientID integer NOT NULL,

  NutrientID integer NOT NULL,

  Quantity decimal NOT NULL,
  FOREIGN KEY(IngredientID) REFERENCES Ingredients(IngredientID)
  FOREIGN KEY(NutrientID) REFERENCES Nutrients(NutrientID)
);
