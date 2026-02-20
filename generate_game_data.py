import numpy as np
import json
import os

# 설정
VECTORS_PATH = 'ko_game_vectors.json'
WORDS_PATH = 'words.json'
ANSWERS_PATH = 'answers.json'
OUTPUT_DIR = 'game_data'

# 데이터 로드
print("벡터 데이터 로딩 중...")
with open(VECTORS_PATH, 'r', encoding='utf-8') as f:
    vectors_raw = json.load(f)

vectors = {word: np.array(vec) for word, vec in vectors_raw.items()}

with open(WORDS_PATH, 'r', encoding='utf-8') as f:
    word_list = json.load(f)

with open(ANSWERS_PATH, 'r', encoding='utf-8') as f:
    answer_list = json.load(f)

print(f"벡터: {len(vectors)}개, 단어: {len(word_list)}개, 정답: {len(answer_list)}개")

# 코사인 유사도 함수
def cosine_similarity(vec_a, vec_b):
    dot = np.dot(vec_a, vec_b)
    norm = np.linalg.norm(vec_a) * np.linalg.norm(vec_b)
    if norm == 0:
        return 0.0
    return float(dot / norm)

# 정답별 유사도 순위 계산
os.makedirs(OUTPUT_DIR, exist_ok=True)

for day_num, answer in enumerate(answer_list, 1):
    print(f"[{day_num}/{len(answer_list)}] 정답: {answer}")

    if answer not in vectors:
        print(f"  ⚠️ 정답 '{answer}'의 벡터가 없습니다. 스킵.")
        continue

    answer_vec = vectors[answer]

    rankings = []
    for word in word_list:
        if word not in vectors:
            continue
        sim = cosine_similarity(answer_vec, vectors[word])
        rankings.append({
            "word": word,
            "similarity": round(sim, 4)
        })

    # 유사도 내림차순 정렬 → 순위 부여
    rankings.sort(key=lambda x: x["similarity"], reverse=True)
    for i, item in enumerate(rankings):
        item["rank"] = i + 1

    # JSON 저장
    output_path = os.path.join(OUTPUT_DIR, f'game_day_{day_num:03d}.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            "answer": answer,
            "total_words": len(rankings),
            "rankings": rankings
        }, f, ensure_ascii=False, indent=2)

print(f"\n완료! {OUTPUT_DIR}/ 에 {len(answer_list)}개 파일 생성됨")
