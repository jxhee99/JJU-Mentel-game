# 🎮 Discord 시맨틀 게임 봇

한국어 단어 유사도 추측 게임을 Discord에서 즐기세요!

## ✨ 특징

- 🔒 **완전한 개인정보 보호**: Ephemeral 메시지로 본인만 결과 확인
- 📊 **4,131개 한국어 단어**: FastText 기반 의미 유사도 계산
- 🎯 **365일 매일 다른 정답**: 1년치 게임 데이터
- 🆓 **완전 무료**: Oracle Cloud 무료 서버에서 운영

## 📋 명령어

| 명령어 | 설명 |
|--------|------|
| `/guess 단어` | 단어 추측 (본인만 결과 표시) |
| `/status` | 오늘의 진행 상황 확인 |
| `/giveup` | 포기하고 정답 확인 |
| `/help` | 도움말 |

## 🚀 빠른 시작

### 1. 필수 준비물
- Python 3.8 이상
- Discord 계정 및 서버 관리자 권한
- (배포용) Oracle Cloud 무료 계정

### 2. Discord 봇 생성

1. [Discord Developer Portal](https://discord.com/developers/applications) 접속
2. **New Application** 클릭
3. 봇 이름 입력 (예: "시맨틀봇")
4. 좌측 **Bot** 메뉴 클릭
5. **Reset Token** → 토큰 복사 (나중에 사용)
6. **Privileged Gateway Intents** 활성화:
   - ✅ MESSAGE CONTENT INTENT

### 3. 봇 서버 초대

1. 좌측 **OAuth2** → **URL Generator**
2. Scopes:
   - ✅ `bot`
   - ✅ `applications.commands`
3. Bot Permissions:
   - ✅ Send Messages
   - ✅ Use Slash Commands
4. 생성된 URL로 접속 → 내 서버에 봇 초대

### 4. 로컬 설정

```bash
# 1. 저장소 클론 또는 다운로드
cd semantle-game

# 2. 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 패키지 설치
pip install -r requirements.txt

# 4. 환경 변수 설정
cp .env.example .env
# .env 파일을 열어서 DISCORD_BOT_TOKEN에 봇 토큰 입력

# 5. 봇 실행
python bot.py
```

### 5. 테스트

Discord 서버에서:
```
/help
/guess 사과
/status
```

## 📁 파일 구조

```
semantle-game/
├── bot.py                      # Discord 봇 메인 코드
├── requirements.txt            # Python 패키지
├── .env                        # 환경 변수 (생성 필요)
├── .env.example               # 환경 변수 예시
├── game_data/                 # 365일치 게임 데이터
│   ├── game_day_001.json
│   ├── game_day_002.json
│   └── ...
├── words.json                 # 단어 리스트 (4,131개)
├── answers.json               # 정답 리스트 (365개)
├── ko_game_vectors.json       # FastText 벡터 데이터
├── extract_vectors.py         # 벡터 추출 스크립트
├── generate_game_data.py      # 게임 데이터 생성 스크립트
└── test_game.py              # 로컬 테스트용
```

## 🌐 Oracle Cloud 배포

### 1. Oracle Cloud 인스턴스 생성

1. [Oracle Cloud](https://www.oracle.com/cloud/free/) 가입
2. VM 인스턴스 생성:
   - Shape: **VM.Standard.A1.Flex** (Always Free)
   - CPU: 2 OCPU
   - RAM: 12 GB
   - OS: Ubuntu 22.04 (ARM)

### 2. 서버 초기 설정

```bash
# SSH 접속 후
sudo apt update && sudo apt upgrade -y

# Python 및 필요 패키지 설치
sudo apt install -y python3 python3-pip python3-venv git

# 프로젝트 업로드
scp -r semantle-game/ ubuntu@서버IP:~/
```

### 3. 서버에서 봇 실행

```bash
cd ~/semantle-game

# 가상환경 생성
python3 -m venv venv
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt

# .env 파일 생성 및 토큰 설정
nano .env
# DISCORD_BOT_TOKEN=your_token_here 입력

# 백그라운드 실행 (systemd 사용)
sudo nano /etc/systemd/system/semantle-bot.service
```

### 4. systemd 서비스 설정

`/etc/systemd/system/semantle-bot.service` 파일 내용:

```ini
[Unit]
Description=Discord Semantle Game Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/semantle-game
Environment="PATH=/home/ubuntu/semantle-game/venv/bin"
ExecStart=/home/ubuntu/semantle-game/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

서비스 시작:
```bash
sudo systemctl daemon-reload
sudo systemctl enable semantle-bot
sudo systemctl start semantle-bot

# 상태 확인
sudo systemctl status semantle-bot

# 로그 확인
sudo journalctl -u semantle-bot -f
```

## 🔧 커스터마이징

### 게임 시작일 변경

`.env` 파일에서:
```
GAME_START_DATE=2025-02-09
```

### 최대 시도 횟수 변경

```
MAX_ATTEMPTS=300
```

### 정답 추가/변경

1. `answers.json` 수정
2. 벡터 추출 및 게임 데이터 재생성:
```bash
python3 extract_vectors.py
python3 generate_game_data.py
```

## 📊 데이터 통계

- **단어 수**: 4,131개
- **정답 수**: 365개
- **벡터 차원**: 300차원 (FastText)
- **게임 데이터 크기**: ~140MB

## 🐛 문제 해결

### 봇이 응답하지 않음
- Discord Developer Portal에서 **MESSAGE CONTENT INTENT** 활성화 확인
- 봇이 서버에 제대로 초대되었는지 확인
- `/` 입력 시 봇 명령어가 보이는지 확인

### 슬래시 커맨드가 안 보임
- 봇 재시작 후 최대 1시간 대기 (Discord 동기화)
- 봇을 서버에서 킥한 후 재초대

### 게임 데이터 로드 실패
- `game_data/` 디렉토리가 있는지 확인
- 파일 권한 확인: `chmod -R 644 game_data/`

## 📄 라이선스

MIT License

## 🙏 크레딧

- FastText 한국어 벡터: [Facebook Research](https://fasttext.cc/)
- 원작 게임: [Semantle](https://semantle.com/)
- 한국어 버전: [꼬맨틀](https://semantle-ko.newsjel.ly/)

## 📧 문의

이슈가 있으시면 GitHub Issues에 등록해주세요.
