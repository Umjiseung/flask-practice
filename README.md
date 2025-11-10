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

3. 포그라운드 모드로 실행
```bash
docker compose up
```

4. 실행 중인지 컨테이너 확인
```bash
docker ps
```

5. 컨테이너 중지
```bash
docker compose down
```
