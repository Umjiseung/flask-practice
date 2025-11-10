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

3. mysql에 board 테이블 생성
```bash
CREATE DATABASE IF NOT EXISTS board;
USE board;

CREATE TABLE IF NOT EXISTS board (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(50),
    content VARCHAR(255)
);

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
