CREATE DATABASE IF NOT EXISTS master_database;
USE master_database;
DROP TABLE IF EXISTS boardgames;
CREATE TABLE boardgames (
  id int DEFAULT NULL,
  name text,
  year_published text,
  min_players int,
  max_players int,
  play_time int,
  min_age int,
  users_rated text,
  rating_average text,
  bgg_rank text,
  complexity_average text,
  owned_users text,
  mechanics text,
  domains text,
  categories text,
  statistical_data text,
  qualitative_data text,
  image_data text,
  users_commented text,
  comments text
);