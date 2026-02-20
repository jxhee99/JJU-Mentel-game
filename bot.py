#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Discord 시맨틀 게임 봇
Ephemeral 메시지를 사용하여 개인 정보 보호
"""

import discord
from discord import app_commands
from discord.ext import commands
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 봇 설정
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GAME_START_DATE = datetime.strptime(os.getenv('GAME_START_DATE', '2025-02-09'), '%Y-%m-%d')
MAX_ATTEMPTS = int(os.getenv('MAX_ATTEMPTS', '100'))

# 봇 인텐트 설정
# 슬래시 커맨드만 사용하므로 기본 인텐트만 필요
intents = discord.Intents.default()

# 봇 생성
bot = commands.Bot(command_prefix='!', intents=intents)

# 유저별 게임 상태 저장 (메모리 기반)
# 형식: {day_num: {user_id: {attempts: int, guesses: [str], solved: bool, best_rank: int}}}
game_states = {}


def get_today_game_data():
    """오늘의 게임 데이터 로드"""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    diff_days = (today - GAME_START_DATE).days
    day_num = (diff_days % 365) + 1

    file_path = f'game_data/game_day_{day_num:03d}.json'

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return day_num, data


def get_user_state(day_num, user_id):
    """유저의 게임 상태 가져오기"""
    if day_num not in game_states:
        game_states[day_num] = {}

    if user_id not in game_states[day_num]:
        game_states[day_num][user_id] = {
            'attempts': 0,
            'guesses': [],
            'solved': False,
            'best_rank': float('inf'),
            'best_word': None,
            'best_similarity': 0.0
        }

    return game_states[day_num][user_id]


def create_progress_bar(similarity, length=20):
    """유사도 진행 막대 생성"""
    filled = int(similarity * length)
    return '🟩' * filled + '⬛' * (length - filled)


@bot.event
async def on_ready():
    """봇 시작 이벤트"""
    print(f'{bot.user} 봇이 준비되었습니다!')
    print(f'서버: {len(bot.guilds)}개')

    # 슬래시 커맨드 동기화
    try:
        synced = await bot.tree.sync()
        print(f'슬래시 커맨드 {len(synced)}개 동기화 완료')
    except Exception as e:
        print(f'커맨드 동기화 실패: {e}')


@bot.tree.command(name="guess", description="단어를 추측합니다 (본인만 결과를 볼 수 있습니다)")
@app_commands.describe(word="추측할 단어")
async def guess(interaction: discord.Interaction, word: str):
    """단어 추측 커맨드"""

    # 게임 데이터 로드
    try:
        day_num, game_data = get_today_game_data()
    except Exception as e:
        await interaction.response.send_message(
            f"❌ 게임 데이터를 불러오는 중 오류가 발생했습니다: {e}",
            ephemeral=True
        )
        return

    # 유저 상태 가져오기
    user_id = interaction.user.id
    user_state = get_user_state(day_num, user_id)

    # 이미 정답을 맞춘 경우
    if user_state['solved']:
        await interaction.response.send_message(
            f"✅ 이미 정답을 맞추셨습니다! ({user_state['attempts']}번째 시도에 성공)\n"
            f"내일 다시 도전하세요!",
            ephemeral=True
        )
        return

    # 단어가 리스트에 있는지 확인
    word_entry = None
    for entry in game_data['rankings']:
        if entry['word'] == word:
            word_entry = entry
            break

    if not word_entry:
        await interaction.response.send_message(
            f"❌ **'{word}'**는 단어 목록에 없습니다.\n"
            f"다른 단어를 시도해보세요!",
            ephemeral=True
        )
        return

    # 이미 시도한 단어인지 확인
    if word in user_state['guesses']:
        await interaction.response.send_message(
            f"⚠️ **'{word}'**는 이미 시도한 단어입니다.\n"
            f"다른 단어를 시도해보세요!",
            ephemeral=True
        )
        return

    # 시도 횟수 제한
    if user_state['attempts'] >= MAX_ATTEMPTS:
        await interaction.response.send_message(
            f"❌ 최대 시도 횟수({MAX_ATTEMPTS}번)에 도달했습니다.\n"
            f"`/giveup` 명령어로 정답을 확인하거나 내일 다시 도전하세요!",
            ephemeral=True
        )
        return

    # 시도 기록
    user_state['attempts'] += 1
    user_state['guesses'].append(word)
    if word_entry['rank'] < user_state['best_rank']:
        user_state['best_rank'] = word_entry['rank']
        user_state['best_word'] = word
        user_state['best_similarity'] = word_entry['similarity']

    # 결과 생성
    similarity = word_entry['similarity'] * 100
    rank = word_entry['rank']

    # 진행 막대
    bar = create_progress_bar(word_entry['similarity'])

    # 정답인 경우
    if rank == 1:
        user_state['solved'] = True

        embed = discord.Embed(
            title="🎉 정답입니다!",
            description=f"정답: **{word}**",
            color=discord.Color.gold()
        )
        embed.add_field(name="시도 횟수", value=f"{user_state['attempts']}번", inline=True)
        embed.add_field(name="Day", value=f"{day_num}", inline=True)
        embed.set_footer(text="축하합니다! 내일 다시 도전하세요!")

        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    # 정답이 아닌 경우
    embed = discord.Embed(
        title=f"단어: {word}",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="📊 유사도",
        value=f"**{similarity:.2f}%**",
        inline=True
    )

    embed.add_field(
        name="🏆 순위",
        value=f"**{rank}위**",
        inline=True
    )

    embed.add_field(
        name="\u200b",  # 빈 필드로 줄바꿈
        value="\u200b",
        inline=False
    )

    embed.add_field(
        name="진행도",
        value=bar,
        inline=False
    )

    embed.add_field(
        name="🔢 시도",
        value=f"{user_state['attempts']}번",
        inline=True
    )

    # 최고 순위 표시 (단어 + 유사도 포함)
    best_rank_text = f"{user_state['best_rank']}위"
    if user_state['best_word']:
        best_rank_text += f" : {user_state['best_word']} ({user_state['best_similarity'] * 100:.2f}%)"
1
    embed.add_field(
        name="🎯 최고 순위",
        value=best_rank_text,
        inline=True
    )

    # 힌트 메시지
    hint = ""
    if rank <= 10:
        hint = "🔥🔥🔥 정말 가깝습니다!"
    elif rank <= 50:
        hint = "🔥🔥 매우 가깝습니다!"
    elif rank <= 100:
        hint = "🔥 아주 가깝습니다!"
    elif rank <= 500:
        hint = "🌡️ 점점 따뜻해지고 있어요"
    else:
        hint = "❄️ 아직 멀어요"

    if hint:
        embed.add_field(
            name="힌트",
            value=hint,
            inline=False
        )

    embed.set_footer(text=f"Day {day_num} • 남은 시도: {MAX_ATTEMPTS - user_state['attempts']}번")

    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="status", description="오늘의 게임 진행 상황을 확인합니다")
async def status(interaction: discord.Interaction):
    """게임 상태 확인 커맨드"""

    try:
        day_num, game_data = get_today_game_data()
    except Exception as e:
        await interaction.response.send_message(
            f"❌ 게임 데이터를 불러오는 중 오류가 발생했습니다: {e}",
            ephemeral=True
        )
        return

    user_id = interaction.user.id
    user_state = get_user_state(day_num, user_id)

    if user_state['attempts'] == 0:
        embed = discord.Embed(
            title="📋 게임 상태",
            description=f"**{interaction.user.name}**님은 오늘 아직 시도하지 않았습니다.",
            color=discord.Color.greyple()
        )
        embed.add_field(name="시작하기", value="`/guess 단어`로 시작하세요!", inline=False)
    else:
        embed = discord.Embed(
            title=f"📋 {interaction.user.name}님의 오늘 현황",
            color=discord.Color.green() if user_state['solved'] else discord.Color.blue()
        )

        embed.add_field(name="Day", value=f"{day_num}", inline=True)
        embed.add_field(name="시도 횟수", value=f"{user_state['attempts']}번", inline=True)

        # 최고 순위 표시 (단어 + 유사도 포함)
        best_rank_text = f"{user_state['best_rank']}위"
        if user_state['best_word']:
            best_rank_text += f" : {user_state['best_word']} ({user_state['best_similarity'] * 100:.2f}%)"
        embed.add_field(name="최고 순위", value=best_rank_text, inline=True)

        status_text = "✅ 정답 맞춤!" if user_state['solved'] else "🔄 진행 중"
        embed.add_field(name="상태", value=status_text, inline=False)

        if not user_state['solved']:
            embed.add_field(
                name="최근 시도 단어",
                value=", ".join(user_state['guesses'][-5:]) if user_state['guesses'] else "없음",
                inline=False
            )

    embed.set_footer(text="매일 자정에 새로운 단어로 리셋됩니다")

    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="giveup", description="포기하고 정답을 확인합니다")
async def giveup(interaction: discord.Interaction):
    """포기 커맨드"""

    try:
        day_num, game_data = get_today_game_data()
    except Exception as e:
        await interaction.response.send_message(
            f"❌ 게임 데이터를 불러오는 중 오류가 발생했습니다: {e}",
            ephemeral=True
        )
        return

    user_id = interaction.user.id
    user_state = get_user_state(day_num, user_id)

    if user_state['solved']:
        await interaction.response.send_message(
            f"✅ 이미 정답을 맞추셨습니다: **{game_data['answer']}**",
            ephemeral=True
        )
        return

    # 포기 처리
    user_state['solved'] = True

    embed = discord.Embed(
        title="😔 포기하셨습니다",
        description=f"오늘의 정답: **{game_data['answer']}**",
        color=discord.Color.red()
    )

    embed.add_field(name="시도 횟수", value=f"{user_state['attempts']}번", inline=True)

    # 최고 순위 표시 (단어 + 유사도 포함)
    best_rank_text = f"{user_state['best_rank']}위"
    if user_state['best_word']:
        best_rank_text += f" : {user_state['best_word']} ({user_state['best_similarity'] * 100:.2f}%)"
    embed.add_field(name="최고 순위", value=best_rank_text, inline=True)

    embed.set_footer(text="내일 다시 도전하세요!")

    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="help", description="게임 설명 및 도움말을 확인합니다")
async def help_command(interaction: discord.Interaction):
    """도움말 커맨드"""

    embed = discord.Embed(
        title="📖 시맨틀 게임 도움말",
        description="매일 하나의 비밀 단어가 정해집니다.\n"
                   "단어를 추측하면 정답과의 **의미 유사도**와 **순위**를 알려드립니다.",
        color=discord.Color.purple()
    )

    embed.add_field(
        name="📝 명령어",
        value=(
            "`/guess 단어` - 단어 추측\n"
            "`/status` - 오늘 내 현황\n"
            "`/giveup` - 포기 (정답 공개)\n"
            "`/help` - 이 도움말"
        ),
        inline=False
    )

    embed.add_field(
        name="📊 유사도 해석",
        value=(
            "🔥🔥🔥 10위 이내 - 정말 가깝습니다!\n"
            "🔥🔥 50위 이내 - 매우 가깝습니다!\n"
            "🔥 100위 이내 - 아주 가깝습니다!\n"
            "🌡️ 500위 이내 - 점점 따뜻해지고 있어요\n"
            "❄️ 500위 밖 - 아직 멀어요"
        ),
        inline=False
    )

    embed.add_field(
        name="🔒 개인정보 보호",
        value="모든 게임 결과는 **본인만** 볼 수 있습니다!\n다른 사람에게는 보이지 않으니 안심하세요.",
        inline=False
    )

    embed.add_field(
        name="⏰ 리셋",
        value="매일 자정(00:00)에 새로운 단어로 리셋됩니다.",
        inline=False
    )

    embed.set_footer(text="행운을 빕니다! 🍀")

    await interaction.response.send_message(embed=embed, ephemeral=True)


# 봇 실행
if __name__ == '__main__':
    if not TOKEN:
        print("❌ 오류: DISCORD_BOT_TOKEN이 설정되지 않았습니다.")
        print(".env 파일을 생성하고 토큰을 설정하세요.")
        exit(1)

    print("🤖 봇을 시작합니다...")
    bot.run(TOKEN)
