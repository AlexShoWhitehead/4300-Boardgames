CREATE DATABASE IF NOT EXISTS boardgamesdb;

USE boardgamesdb;
DROP TABLE IF EXISTS boardgames;

CREATE TABLE boardgames(
    id int,
    named text,
    descr text,
    year_published int,
    min_players int,
    max_players int,
    play_time int,
    min_age int,
    users_rated int,
    rating_average text,
    bgg_rank int,
    complexity_average text,
    owned_users int,
    mechanics text,
    domains text,
    categories text,
    statistical_data text,
    qualitative_data text,
    image_data text,
    users_commented int,
    comments text
);
-- INSERT INTO episodes VALUE(174430, 'Gloomhaven', 2017, 1, 4, 120, 14, 57372, '8.6', 3, '3.86', 90020, 'Action Queue', 'Strategy games', 'Adventure', 'rating_bayes_average: 8.39527', 'hi', 'https://cf.geekdo-images.com/sZYp_3BTDGjh2unaZfZmuA__thumb/img/veqFeP4d_3zNhFc3GNBkV95rBEQ=/fit-in/200x150/filters:strip_icc()/pic2437871.jpg', 'image': 'https://cf.geekdo-images.com/sZYp_3BTDGjh2unaZfZmuA__original/img/7d-lj5Gd1e8PFnD97LYFah2c45M=/0x0/filters:format(jpeg)/pic2437871.jpg', 20, "cool");
