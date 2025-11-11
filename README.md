# docker를 이용하여 mysql, flask 실행

## Docker Compose 빌드

1. 도커 이미지를 새로 빌드하려면 다음 명령어를 사용합니다.
```bash 
docker compose build
```

2. 백그라운드(Detached) 모드로 실행
```bash
docker compose up -d
```

3. mysql에서 테이블 생성
```bash
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

```

4. 포그라운드 모드로 실행
```bash
docker compose up
```

5. 실행 중인지 컨테이너 확인
```bash
docker ps
```

6. 컨테이너 중지
```bash
docker compose down
```
