CREATE TABLE "users" (
  "username" VARCHAR NOT NULL,
  "name" VARCHAR NOT NULL,
  "email" VARCHAR NOT NULL,
  "password" INTEGER NOT NULL
);

CREATE TABLE "books" (
  "isbn" VARCHAR PRIMARY KEY NOT NULL,
  "title" VARCHAR NOT NULL,
  "author" VARCHAR NOT NULL,
  "year" INTEGER NOT NULL
);

CREATE TABLE "reviews" (
  "isbn" VARCHAR NOT NULL,
  "username" VARCHAR NOT NULL,
  "review" VARCHAR NOT NULL,
  "rate" INTEGER NOT NULL
  unique ("username", "isbn")
);