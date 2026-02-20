#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
게임 로직 테스트 스크립트 (Discord 없이 로컬에서 테스트)
"""

import json
import os
from datetime import datetime, timedelta

# 설정
GAME_DATA_DIR = 'game_data'
CONFIG = {
    "game_start_date": "2025-02-09",
    "max_attempts": 100
}

def get_today_game_data():
    """오늘의 게임 데이터 가져오기"""
    start_date = datetime.strptime(CONFIG["game_start_date"], "%Y-%m-%d")
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    diff_days = (today - start_date).days
    day_num = (diff_days % 365) + 1

    file_path = os.path.join(GAME_DATA_DIR, f'game_day_{day_num:03d}.json')

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return day_num, data

def find_word_info(game_data, word):
    """단어의 순위와 유사도 찾기"""
    for entry in game_data['rankings']:
        if entry['word'] == word:
            return entry
    return None

def main():
    print("=" * 60)
    print("🎮 시맨틀 게임 로직 테스트")
    print("=" * 60)

    # 오늘의 게임 데이터 로드
    day_num, game_data = get_today_game_data()
    answer = game_data['answer']
    total_words = game_data['total_words']

    print(f"\n📅 Day {day_num}")
    print(f"📊 전체 단어 수: {total_words}개")
    print(f"🔒 정답: {answer} (테스트용으로만 표시)")
    print("\n" + "=" * 60)

    # 사용자 상태 시뮬레이션
    user_attempts = 0
    user_guesses = []
    best_rank = float('inf')

    print("\n💡 테스트 명령어:")
    print("  - 단어 입력: 추측할 단어를 입력하세요")
    print("  - 'status': 현재 상태 확인")
    print("  - 'hint': 상위 10개 단어 힌트")
    print("  - 'quit': 종료\n")

    while True:
        guess = input("\n추측할 단어를 입력하세요 > ").strip()

        if not guess:
            continue

        if guess == 'quit':
            print("\n게임을 종료합니다. 안녕히 가세요!")
            break

        if guess == 'status':
            print(f"\n📊 현재 상태:")
            print(f"  시도 횟수: {user_attempts}번")
            print(f"  최고 순위: {best_rank if best_rank != float('inf') else '없음'}")
            print(f"  시도한 단어: {', '.join(user_guesses) if user_guesses else '없음'}")
            continue

        if guess == 'hint':
            print(f"\n💡 힌트 - 상위 10개 단어:")
            for i, entry in enumerate(game_data['rankings'][:10], 1):
                if i == 1:
                    print(f"  {i}. {entry['word']} (정답)")
                else:
                    print(f"  {i}. {entry['word']} - 유사도: {entry['similarity']*100:.2f}%")
            continue

        # 중복 체크
        if guess in user_guesses:
            print(f"⚠️ '{guess}'는 이미 시도한 단어입니다.")
            continue

        # 단어 찾기
        word_info = find_word_info(game_data, guess)

        if not word_info:
            print(f"❌ '{guess}'는 단어 목록에 없습니다.")
            continue

        # 시도 기록
        user_attempts += 1
        user_guesses.append(guess)
        if word_info['rank'] < best_rank:
            best_rank = word_info['rank']

        # 결과 표시
        similarity = word_info['similarity'] * 100
        rank = word_info['rank']

        # 진행 막대
        bar_length = 20
        filled = int(word_info['similarity'] * bar_length)
        bar = '🟩' * filled + '⬛' * (bar_length - filled)

        print(f"\n{'='*60}")
        if rank == 1:
            print(f"🎉 정답입니다!")
            print(f"\n정답: {guess}")
            print(f"시도 횟수: {user_attempts}번")
            print(f"\n축하합니다! 🏆")
            print(f"{'='*60}")
            break
        else:
            print(f"단어: {guess}")
            print(f"📊 유사도: {similarity:.2f}% | 순위: {rank} / {total_words}")
            print(f"{bar}")
            print(f"🔢 시도: {user_attempts}번 | 최고 순위: {best_rank}위")

            # 힌트 메시지
            if rank <= 10:
                print(f"🔥🔥🔥 정말 가깝습니다!")
            elif rank <= 50:
                print(f"🔥🔥 매우 가깝습니다!")
            elif rank <= 100:
                print(f"🔥 아주 가깝습니다!")
            elif rank <= 500:
                print(f"🌡️ 점점 따뜻해지고 있어요")
            else:
                print(f"❄️ 아직 멀어요")
        print(f"{'='*60}")

if __name__ == '__main__':
    main()
