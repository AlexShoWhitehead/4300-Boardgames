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
INSERT INTO boardgames VALUES 
(174430,'Gloomhaven','2017',1,4,120,14,'57372','8.62868','3','3,86','90020',"['Action Queue']",'Strategy Games, Thematic Games',"blah","blah","{'description':'hi'}",{'image':'https://www.cs.cornell.edu/courses/cs5152/2022sp/staff/photos/walker.png'}, "blah", "oof");
INSERT INTO boardgames VALUES 
(174430,'Gloomhaven','2017',1,4,120,14,'57372','8.62868','3','3,86','90020',"['Action Queue']",'Strategy Games, Thematic Games',"blah","blah","{'description':'hi'}","blah", "blah", "oof");
INSERT INTO boardgames VALUES 
(174430,'Gloomhaven','2017',1,4,120,14,'57372','8.62868','3','3,86','90020',"['Action Queue']",'Strategy Games, Thematic Games',"blah","blah","{'description':'hi'}","blah", "blah", "oof");