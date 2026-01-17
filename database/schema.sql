CREATE DATABASE spotify_churn;
USE spotify_churn;

CREATE TABLE users (
  user_id INT PRIMARY KEY AUTO_INCREMENT,
  subscription_type VARCHAR(20),
  age INT,
  country VARCHAR(30),
  avg_listening_hours_per_week FLOAT,
  login_frequency_per_week INT,
  songs_skipped_per_week INT,
  playlists_created INT,
  days_since_last_login INT,
  churn INT
);
