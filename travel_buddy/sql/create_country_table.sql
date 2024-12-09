DROP TABLE IF EXISTS countries;
CREATE TABLE countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country TEXT NOT NULL UNIQUE,
    capital TEXT NOT NULL UNIQUE,
    languages TEXT NOT NULL,
    currency TEXT NOT NULL,
    region TEXT CHECK(region IN ('Africa','Americas', 'Asia', 'Europe','Oceania')),
    countrycode TEXT NOT NULL UNIQUE,
    deleted BOOLEAN DEFAULT FALSE
);