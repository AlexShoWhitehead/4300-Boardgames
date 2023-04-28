CREATE DATABASE IF NOT EXISTS master_database;

USE master_database;
DROP TABLE IF EXISTS 'boardgames';

CREATE TABLE boardgames (
  id int DEFAULT NULL,
  name text,
  year_published text,
  min_players text,
  max_players text,
  play_time text,
  min_age text,
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
  image_data text
);

INSERT INTO 'boardgames'(id, name, year_published, min_players, max_players, play_time, min_age, users_rated, rating_average, bgg_rank, complexity_average, owned_users, mechanics, domains, categories, statistical_data, qualitative_data, image_data) VALUES (174430,'Gloomhaven',
'2017',
'1',
'4',
'120',
'14',
'57372',
'8.62868',
'3',
'3,86',
'90020',
"['Action Queue']",
'Strategy Games, Thematic Games',
"['Adventure\']",
"{\'rating_bayes_average\': 8.39527, \'rating_stdev\': 1.74969, \'rating_median\': 0.0, \'rating_num_weights\': 2376, \'rating_average_weight\': 3.8893}",
"{\'alternative_names\': [\'Gloomhaven, aventures à Havrenuit\', \'Gloomhaven: Мрачная Гавань\', \'Homályrév\', \'グルームヘイヴン\', \'幽港迷城\', \'글룸헤이븐\'], \'description\': \'Gloomhaven  is a game of Euro-inspired tactical combat in a persistent world of shifting motives. Players will take on the role of a wandering adventurer with their own special set of skills and their own reasons for traveling to this dark corner of the world. Players must work together out of necessity to clear out menacing dungeons and forgotten ruins. In the process, they will enhance their abilities with experience and loot, discover new locations to explore and plunder, and expand an ever-branching story fueled by the decisions they make.\n\nThis is a game with a persistent and changing world that is ideally played over many game sessions. After a scenario, players will make decisions on what to do, which will determine how the story continues, kind of like a “Choose Your Own Adventure” book. Playing through a scenario is a cooperative affair where players will fight against automated monsters using an innovative card system to determine the order of play and what a player does on their turn.\n\nEach turn, a player chooses two cards to play out of their hand. The number on the top card determines their initiative for the round. Each card also has a top and bottom power, and when it is a player \'s turn in the initiative order, they determine whether to use the top power of one card and the bottom power of the other, or vice-versa. Players must be careful, though, because over time they will permanently lose cards from their hands. If they take too long to clear a dungeon, they may end up exhausted and be forced to retreat.\n\n\', \'families\': [\'Category: Dungeon Crawler\', \'Components: Miniatures\', \'Components: Multi-Use Cards\', \'Components: Standees\', \'Creatures: Demons\', \'Creatures: Dragons\', \'Creatures: Monsters\', \'Crowdfunding: Kickstarter\', \'Digital Implementations: Steam\', \'Digital Implementations: TableTop Simulator Mod (TTS)\', \'Game: Gloomhaven\', \'Mechanism: Campaign Games\', \'Mechanism: Legacy\', \'Misc: Forteller Audio Narration\', \'Misc: Made by Panda\', \'Players: Games with Solitaire Rules\'], \'is_expansion\': False, \'expansions\': [\'The Crimson Scales\', \'The Crimson Scales: Class Pack Add-on\', \'The Crimson Scales: Trail of Ashes\', \'Gloomhaven: Assault on the Morning Star (Promo Scenario)\', \'Gloomhaven: Beyond the End of the World (Promo Scenario)\', \'Gloomhaven: Envelope X Reward\', \'Gloomhaven: Forgotten Circles\', \'Gloomhaven: Memories of Gloomhaven (Promo Scenario)\', \'Gloomhaven: Return of the Lost Cabal (Promo Scenario)\', \'Gloomhaven: Secrets of the Lost Cabal (Promo Scenario)\', \'Gloomhaven: Solo Scenarios\', \'Gloomhaven: The Catacombs of Chaos (Promo Scenario)\', \'Gloomhaven: The End of the World (Promo Scenario)\', \'Gloomhaven: The Lucky Meeple (Promo Scenario)\', \'Gloomhaven: The Tower of Misfortune (Promo Scenario)\', \'Gloomhaven: Twilight of the Lost Cabal (Promo Scenario)\'], \'expands\': []}",
"{\'thumbnail\': \'https://cf.geekdo-images.com/sZYp_3BTDGjh2unaZfZmuA__thumb/img/veqFeP4d_3zNhFc3GNBkV95rBEQ=/fit-in/200x150/filters:strip_icc()/pic2437871.jpg\', \'image\': \'https://cf.geekdo-images.com/sZYp_3BTDGjh2unaZfZmuA__original/img/7d-lj5Gd1e8PFnD97LYFah2c45M=/0x0/filters:format(jpeg)/pic2437871.jpg\'}");

