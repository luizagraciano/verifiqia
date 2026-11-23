INSERT OR IGNORE INTO activity_content (id, activity_id, instruction, answer, resources) VALUES
(1, 1, 'Instruction for activity 1', 'Answer for activity 1', 'Resources for activity 1'),
(2, 2, 'Instruction for activity 2', 'Answer for activity 2', 'Resources for activity 2'),
(3, 3, 'Instruction for activity 3', 'Answer for activity 3', 'Resources for activity 3');

INSERT OR IGNORE INTO activity_list (id, name, description, tag, difficulty) VALUES
(1, 'Activity 1', 'Description for activity 1', 'Ética', 'easy'),
(2, 'Activity 2', 'Description for activity 2', 'Matemática', 'medium'),
(3, 'Activity 3', 'Description for activity 3', 'História', 'hard');

INSERT OR IGNORE INTO offline_activity_content (id, activity_id, instruction, answer, resources) VALUES
(1, 1, 'Instruction for offline activity 1', 'Answer for offline activity 1', 'Resources for offline activity 1'),
(2, 2, 'Instruction for offline activity 2', 'Answer for offline activity 2', 'Resources for offline activity 2'),
(3, 3, 'Instruction for offline activity 3', 'Answer for offline activity 3', 'Resources for offline activity 3');

INSERT OR IGNORE INTO offline_activity_list (id, name, description, tag, difficulty) VALUES
(1, 'Offline Activity 1', 'Description for offline activity 1', 'Matemática', 'easy'),
(2, 'Offline Activity 2', 'Description for offline activity 2', 'Ética', 'medium'),
(3, 'Offline Activity 3', 'Description for offline activity 3', 'História', 'hard');