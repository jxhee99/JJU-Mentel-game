#!/bin/bash
# Discord 시맨틀 봇 빠른 설정 스크립트

echo "========================================="
echo "Discord 시맨틀 게임 봇 설정"
echo "========================================="

# Python 버전 확인
echo -e "\n[1/5] Python 버전 확인..."
python3 --version || { echo "❌ Python 3가 설치되지 않았습니다."; exit 1; }

# 가상환경 생성
echo -e "\n[2/5] 가상환경 생성..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ 가상환경 생성 완료"
else
    echo "✅ 가상환경이 이미 존재합니다"
fi

# 가상환경 활성화
echo -e "\n[3/5] 가상환경 활성화..."
source venv/bin/activate

# 패키지 설치
echo -e "\n[4/5] 필요한 패키지 설치..."
pip install -r requirements.txt

# .env 파일 생성
echo -e "\n[5/5] 환경 변수 설정..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ .env 파일이 생성되었습니다"
    echo ""
    echo "⚠️  중요: .env 파일을 열어서 DISCORD_BOT_TOKEN을 설정하세요!"
    echo "    nano .env"
else
    echo "✅ .env 파일이 이미 존재합니다"
fi

echo ""
echo "========================================="
echo "✅ 설정 완료!"
echo "========================================="
echo ""
echo "다음 단계:"
echo "  1. .env 파일 편집: nano .env"
echo "  2. DISCORD_BOT_TOKEN 설정"
echo "  3. 봇 실행: python bot.py"
echo ""
