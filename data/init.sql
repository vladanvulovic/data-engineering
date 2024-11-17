CREATE TABLE registration_data (
                                   user_id UUID PRIMARY KEY,
                                   country VARCHAR(50),
                                   registration_date_local_timezone TIMESTAMP,
                                   device VARCHAR(50)
);

CREATE TABLE session_data (
                              user_id UUID,
                              date DATE,
                              session_count INT,
                              time_spent_in_game BIGINT,
                              PRIMARY KEY (user_id, date)
);

CREATE TABLE match_data (
                            user_id UUID,
                            date DATE,
                            total_duration BIGINT,
                            total_points_home INT,
                            total_points_away INT,
                            PRIMARY KEY (user_id, date)
);

-- TODO create indexes
CREATE INDEX idx_session_user_id ON session_data (user_id);
CREATE INDEX idx_session_date ON session_data (date);
CREATE INDEX idx_match_user_id ON match_data (user_id);
CREATE INDEX idx_match_date ON match_data (date);
