# 🎮 Discord 시맨틀 게임 - 완벽 가이드

> FastText 기반 한국어 단어 유사도 추측 게임

## 📋 목차

- [프로젝트 개요](#프로젝트-개요)
- [완성된 것들](#완성된-것들)
- [로컬 실행하기](#로컬-실행하기)
- [Discord 설정](#discord-설정)
- [게임 플레이](#게임-플레이)
- [문제 해결](#문제-해결)
- [서버 배포](#서버-배포)
- [고급 설정](#고급-설정)

---

## 프로젝트 개요

### ✨ 특징

- **4,131개 한국어 단어** - FastText 300차원 벡터 기반
- **365일 매일 다른 정답** - 1년치 게임 데이터
- **완벽한 개인정보 보호** - Ephemeral 메시지 (본인만 결과 확인)
- **아름다운 UI** - Discord Embed로 깔끔한 표시
- **완전 무료 운영** - Oracle Cloud 무료 서버 지원

### 🎯 게임 방식

1. 매일 자정 새로운 정답 단어가 정해짐
2. 사용자가 단어를 추측하면 정답과의 **의미 유사도**와 **순위** 표시
3. 유사도가 높을수록 정답에 가까움
4. 모든 결과는 **본인만** 볼 수 있음 (Ephemeral 메시지)

---

## 완성된 것들

### 📁 파일 구조

```
semantle-game/
├── bot.py                      # Discord 봇 메인 코드 ⭐
├── requirements.txt            # Python 패키지 목록
├── .env.example               # 환경 변수 예시
├── setup.sh                   # 빠른 설정 스크립트
├── README.md                  # 상세 문서
├── GUIDE.md                   # 이 파일
│
├── game_data/                 # 365일치 게임 데이터 (각 343KB)
│   ├── game_day_001.json     # Day 1 정답: "희열"
│   ├── game_day_002.json     # Day 2 정답: "커튼"
│   └── ... (365개)
│
├── words.json                 # 단어 리스트 (4,131개, 55KB)
├── answers.json               # 정답 리스트 (365개, 4.4KB)
├── ko_game_vectors.json       # FastText 벡터 (10MB)
├── cc.ko.300.vec              # FastText 원본 (4.2GB, 재사용용)
│
└── 유틸리티 스크립트
    ├── extract_vectors.py     # 벡터 추출 (정답 추가 시)
    ├── generate_game_data.py  # 게임 데이터 생성 (정답 추가 시)
    └── test_game.py          # 로컬 테스트용
```

### 📊 데이터 통계

| 항목 | 수량 | 크기 |
|------|------|------|
| 단어 수 | 4,131개 | 55KB |
| 정답 수 | 365개 | 4.4KB |
| 게임 데이터 | 365 파일 | ~140MB |
| 벡터 데이터 | 4,131개 | 10MB |
| FastText 원본 | 200만 단어 | 4.2GB |
| **총 디스크 사용** | - | **~4.4GB** |

---

## 로컬 실행하기

### 1️⃣ 사전 준비

**필수 프로그램:**
- Python 3.8 이상
- pip (Python 패키지 관리자)
- Discord 계정

**확인:**
```bash
python3 --version  # Python 3.8+ 확인
pip3 --version     # pip 확인
```

### 2️⃣ 프로젝트 설정

```bash
# 1. 프로젝트 폴더로 이동
cd ~/Documents/MYPROJECT/semantle-game

# 2. 빠른 설정 실행
chmod +x setup.sh
./setup.sh
```

**setup.sh가 하는 일:**
- ✅ Python 버전 확인
- ✅ 가상환경 생성 (`venv/`)
- ✅ 필요 패키지 설치 (`discord.py`, `python-dotenv`, `numpy`)
- ✅ `.env` 파일 생성

### 3️⃣ 환경 변수 설정

```bash
# .env 파일 열기
nano .env
```

**입력할 내용:**
```bash
DISCORD_BOT_TOKEN=여기에_봇_토큰_입력
GAME_START_DATE=2025-02-09
MAX_ATTEMPTS=100
```

- **DISCORD_BOT_TOKEN**: Discord Developer Portal에서 발급 (아래 설명)
- **GAME_START_DATE**: 게임 시작 날짜 (Day 1 기준일)
- **MAX_ATTEMPTS**: 최대 시도 횟수

저장: `Ctrl+O` → `Enter` → `Ctrl+X`

### 4️⃣ 봇 실행

```bash
# 가상환경 활성화
source venv/bin/activate

# 봇 실행
python bot.py
```

**정상 실행 시 출력:**
```
🤖 봇을 시작합니다...
<봇이름>#1234 봇이 준비되었습니다!
서버: 1개
슬래시 커맨드 4개 동기화 완료
```

### 5️⃣ 봇 중지

터미널에서:
```
Ctrl + C
```

---

## Discord 설정

### 1️⃣ Discord 봇 생성

1. **[Discord Developer Portal](https://discord.com/developers/applications)** 접속
2. **New Application** 클릭
3. 애플리케이션 이름 입력 (예: "시맨틀봇")
4. **Create** 클릭

### 2️⃣ 봇 설정

1. 좌측 메뉴에서 **Bot** 클릭
2. **Reset Token** 클릭 → 토큰 복사
   - ⚠️ **절대 공개하지 마세요!**
   - `.env` 파일에만 저장
3. 아래로 스크롤 → **Privileged Gateway Intents**
   - ❌ MESSAGE CONTENT INTENT (꺼둬도 됨)
   - 슬래시 커맨드만 사용하므로 불필요
4. **Save Changes**

### 3️⃣ 봇 초대 URL 생성

1. 좌측 메뉴 **OAuth2** → **URL Generator**
2. **SCOPES** 선택:
   - ✅ `bot`
   - ✅ `applications.commands`
3. **BOT PERMISSIONS** 선택:
   - ✅ `Send Messages`
   - ✅ `Use Slash Commands`
4. 하단 **GENERATED URL** 복사

### 4️⃣ 봇을 서버에 초대

1. 복사한 URL을 브라우저에 붙여넣기
2. 서버 선택
3. **승인** 클릭
4. "나는 로봇이 아닙니다" 체크
5. **승인** 완료

### 5️⃣ 봇 온라인 확인

Discord 서버에서:
- 우측 멤버 목록에 봇이 보임
- 이름 옆에 **초록색 불** 🟢 (온라인 상태)

---

## 게임 플레이

### 명령어 목록

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `/guess 단어` | 단어 추측 (본인만 결과 표시) | `/guess 사과` |
| `/status` | 오늘의 진행 상황 확인 | `/status` |
| `/giveup` | 포기하고 정답 확인 | `/giveup` |
| `/help` | 게임 설명 및 도움말 | `/help` |

### 사용 방법

#### 1. 도움말 확인
```
/help
```
→ 게임 설명이 **본인만 보이는** 메시지로 나타남

#### 2. 단어 추측
```
/guess 사과
```

**결과 예시:**
```
단어: 사과
📊 유사도: 45.23%
🏆 순위: 234 / 4131

진행도: 🟩🟩🟩🟩🟩⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛

🔢 시도: 1번 | 🎯 최고 순위: 234위

힌트: ❄️ 아직 멀어요
```

#### 3. 힌트 해석

| 힌트 | 순위 | 의미 |
|------|------|------|
| 🔥🔥🔥 정말 가깝습니다! | 1-10위 | 거의 정답! |
| 🔥🔥 매우 가깝습니다! | 11-50위 | 매우 근접 |
| 🔥 아주 가깝습니다! | 51-100위 | 근접 |
| 🌡️ 점점 따뜻해지고 있어요 | 101-500위 | 중간 |
| ❄️ 아직 멀어요 | 501위 이상 | 멀음 |

#### 4. 정답 맞추기

정답을 맞추면:
```
🎉 정답입니다!

정답: 희열
시도 횟수: 15번
Day: 1

축하합니다! 내일 다시 도전하세요! 🏆
```

### 게임 규칙

1. **매일 자정(00:00)** 새로운 단어로 리셋
2. **최대 100번** 시도 가능 (변경 가능)
3. **같은 단어 중복 불가**
4. **단어 목록에 있는 단어만** 시도 가능
5. **모든 결과는 본인만 볼 수 있음** (Ephemeral)

### 팁

1. **빠른 입력:**
   - `/` 입력 후 `g`만 입력 → `/guess` 자동 선택
   - 위 화살표 ↑ → 이전 명령어 재사용

2. **전략:**
   - 넓은 범위의 단어부터 시도 (예: 감정, 자연, 사물)
   - 유사도 높은 단어 나오면 → 비슷한 카테고리 시도
   - 상위권 단어 찾으면 → 유사어 집중 공략

3. **개인정보 보호:**
   - 다른 사람은 절대 못 봄!
   - 안심하고 플레이 가능

---

## 문제 해결

### 봇이 실행되지 않아요

#### 에러: `ModuleNotFoundError: No module named 'discord'`
**원인:** 가상환경이 활성화되지 않았거나 패키지 미설치

**해결:**
```bash
# 가상환경 활성화
source venv/bin/activate

# 패키지 재설치
pip install -r requirements.txt
```

#### 에러: `PrivilegedIntentsRequired`
**원인:** MESSAGE CONTENT INTENT 설정 문제

**해결:** 이미 코드에서 수정됨! 그대로 실행하면 됩니다.

만약 계속 에러 나면:
1. Discord Developer Portal → Bot → Privileged Gateway Intents
2. MESSAGE CONTENT INTENT 끄기

#### 에러: `discord.errors.LoginFailure: Improper token has been passed`
**원인:** 봇 토큰이 잘못됨

**해결:**
1. Discord Developer Portal에서 토큰 리셋
2. 새 토큰을 `.env` 파일에 입력
3. 절대 공개하지 말 것!

### 슬래시 커맨드가 안 보여요

#### `/` 입력해도 봇 명령어가 안 나타남

**원인:** Discord 동기화 지연

**해결:**
1. **5분~1시간 대기** (처음 봇 실행 시)
2. Discord 앱 완전 종료 후 재시작
3. 봇 재시작:
   ```bash
   # Ctrl+C로 중지 후
   python bot.py
   ```
4. 여전히 안 되면: 봇을 서버에서 킥 → 재초대

### 게임 데이터 로드 실패

#### 에러: `FileNotFoundError: game_data/game_day_001.json`
**원인:** 게임 데이터 파일이 없거나 경로 문제

**해결:**
```bash
# 현재 위치 확인
pwd
# /Users/juhee/Documents/MYPROJECT/semantle-game 이어야 함

# game_data 폴더 확인
ls -l game_data/game_day_001.json

# 없으면 게임 데이터 재생성
python3 generate_game_data.py
```

### 봇이 응답하지 않아요

#### 명령어 입력했는데 아무 반응 없음

**체크리스트:**
1. **봇이 온라인인가?**
   - 멤버 목록에서 초록불 🟢 확인
   - 터미널에서 봇 실행 중 확인

2. **슬래시 커맨드가 보이나?**
   - `/` 입력 시 명령어 목록 확인
   - 안 보이면 위 "슬래시 커맨드가 안 보여요" 참고

3. **에러 로그 확인**
   - 터미널에서 에러 메시지 확인

### 매일 자정에 리셋이 안 돼요

**원인:** 게임 시작일 설정 문제

**확인:**
```bash
# .env 파일 확인
cat .env
```

**GAME_START_DATE가 올바른지 확인:**
- 오늘이 2025년 2월 11일이면
- GAME_START_DATE=2025-02-09
- → Day 3 (11 - 9 + 1)

---

## 서버 배포

### Oracle Cloud 무료 서버

#### 장점
- ✅ **영구 무료** (Always Free 티어)
- ✅ ARM 기반 VM (4 OCPU, 24GB RAM)
- ✅ 월 10TB 트래픽
- ✅ 충분한 성능

#### 단계별 가이드

**1. Oracle Cloud 가입**
- https://www.oracle.com/cloud/free/
- 카드 등록 필요 (본인 인증용, Always Free 사용 시 청구 없음)

**2. VM 인스턴스 생성**
- Shape: **VM.Standard.A1.Flex** (Always Free Eligible)
- CPU: 2-4 OCPU
- RAM: 12-24 GB
- OS: **Ubuntu 22.04 (ARM)**

**3. 서버 초기 설정**
```bash
# SSH 접속
ssh ubuntu@서버IP

# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# Python 설치
sudo apt install -y python3 python3-pip python3-venv

# 프로젝트 업로드 (로컬에서 실행)
scp -r ~/Documents/MYPROJECT/semantle-game ubuntu@서버IP:~/
```

**4. 서버에서 봇 설정**
```bash
cd ~/semantle-game

# 가상환경 생성
python3 -m venv venv
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt

# .env 파일 생성
nano .env
# 토큰 입력 후 저장
```

**5. systemd 서비스 설정** (24/7 실행)

```bash
sudo nano /etc/systemd/system/semantle-bot.service
```

**파일 내용:**
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

**서비스 시작:**
```bash
# 서비스 등록
sudo systemctl daemon-reload
sudo systemctl enable semantle-bot

# 서비스 시작
sudo systemctl start semantle-bot

# 상태 확인
sudo systemctl status semantle-bot

# 로그 확인
sudo journalctl -u semantle-bot -f
```

**6. 서비스 관리 명령어**
```bash
# 재시작
sudo systemctl restart semantle-bot

# 중지
sudo systemctl stop semantle-bot

# 상태 확인
sudo systemctl status semantle-bot

# 로그 보기
sudo journalctl -u semantle-bot -n 100
```

### 비용

**완전 무료!**
- Oracle Cloud Always Free: $0
- Discord Bot API: $0
- 네트워크 트래픽 (~1GB/월): $0

**주의:**
- Always Free Eligible 인스턴스만 사용
- Paid 리소스 실수로 선택하지 않도록 주의

---

## 고급 설정

### 정답 추가/변경

#### 1. answers.json 수정
```bash
nano answers.json
```

새 정답 추가:
```json
[
  "희열",
  "커튼",
  "선풍기",
  "새로운정답1",  ← 추가
  "새로운정답2"   ← 추가
]
```

#### 2. 벡터 추출
```bash
python3 extract_vectors.py
```
- FastText 원본 (cc.ko.300.vec) 필요
- 새 정답의 벡터 추출

#### 3. 게임 데이터 재생성
```bash
python3 generate_game_data.py
```
- 모든 game_day_XXX.json 파일 재생성
- 약 10-30분 소요

#### 4. 봇 재시작
```bash
# 로컬
Ctrl+C → python bot.py

# 서버
sudo systemctl restart semantle-bot
```

### 게임 설정 변경

**`.env` 파일 수정:**

```bash
# 최대 시도 횟수 변경
MAX_ATTEMPTS=50  # 기본: 100

# 게임 시작일 변경
GAME_START_DATE=2025-03-01
```

변경 후 봇 재시작 필요!

### 단어 추가

**더 많은 단어를 추가하려면:**

1. `words.json`에 단어 추가
2. `extract_vectors.py` 실행 (FastText 벡터 추출)
3. `generate_game_data.py` 실행 (게임 데이터 재생성)

**주의:** FastText에 벡터가 없는 단어는 자동으로 제외됨

### 데이터 백업

**중요 파일 백업:**
```bash
# 백업 디렉토리 생성
mkdir -p backup

# 백업
cp answers.json backup/
cp words.json backup/
cp -r game_data/ backup/
cp ko_game_vectors.json backup/
```

**서버에서 로컬로 백업:**
```bash
scp -r ubuntu@서버IP:~/semantle-game/game_data ~/backup/
```

---

## 📚 참고 자료

### 프로젝트 관련
- **FastText 한국어 벡터:** https://fasttext.cc/
- **Discord.py 문서:** https://discordpy.readthedocs.io/
- **Discord Developer Portal:** https://discord.com/developers/applications

### 게임 영감
- **Semantle (영어):** https://semantle.com/
- **꼬맨틀 (한국어):** https://semantle-ko.newsjel.ly/

### 기술 스택
- **Python 3.8+**
- **discord.py 2.3.0+**
- **FastText 300차원 벡터**
- **NumPy** (벡터 연산)

---

## 🎯 요약

### 로컬 실행 (3단계)
```bash
# 1. 설정
./setup.sh

# 2. 토큰 입력
nano .env

# 3. 실행
source venv/bin/activate
python bot.py
```

### Discord 설정 (4단계)
1. Developer Portal에서 봇 생성
2. 토큰 복사 → `.env` 입력
3. 봇 초대 URL 생성
4. 서버에 초대

### 게임 플레이 (슬래시 커맨드)
- `/guess 단어` - 추측
- `/status` - 상태
- `/help` - 도움말
- `/giveup` - 포기

---

## 💡 팁

1. **가상환경 꼭 활성화!**
   ```bash
   source venv/bin/activate
   ```

2. **토큰 절대 공개 금지!**
   - `.env` 파일에만 저장
   - GitHub 업로드 금지 (.gitignore에 포함됨)

3. **Ephemeral 메시지**
   - 모든 결과는 본인만 볼 수 있음
   - 다른 사람 화면에 안 나타남
   - 정답 스포 걱정 없음!

4. **24/7 운영**
   - Oracle Cloud Always Free 활용
   - systemd로 자동 재시작
   - 완전 무료!

---

**작성일:** 2025-02-11
**버전:** 1.0
**상태:** ✅ 완성 및 테스트 완료

🎮 즐거운 게임 되세요!
