CREATE DATABASE IF NOT EXISTS board;
USE board;

-- Board 테이블
CREATE TABLE IF NOT EXISTS board (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    content VARCHAR(255) NOT NULL,
    likes INT DEFAULT 0 NOT NULL
);

-- Comment 테이블
CREATE TABLE IF NOT EXISTS comment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content VARCHAR(100) NOT NULL,
    likes INT DEFAULT 0 NOT NULL,
    parent_comment_id INT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    board_id INT NOT NULL,
    
    -- Foreign Keys
    FOREIGN KEY (parent_comment_id) REFERENCES comment(id) ON DELETE CASCADE,
    FOREIGN KEY (board_id) REFERENCES board(id) ON DELETE CASCADE
);

-- 인덱스 추가 (성능 향상)
CREATE INDEX idx_comment_board_id ON comment(board_id);
CREATE INDEX idx_comment_parent_id ON comment(parent_comment_id);