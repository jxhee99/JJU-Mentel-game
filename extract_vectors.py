import io
import json
import os

# 설정
VEC_PATH = 'cc.ko.300.vec'
WORDS_PATH = 'words.json'
ANSWERS_PATH = 'answers.json'
OUTPUT_PATH = 'ko_game_vectors.json'

# 게임에 필요한 전체 단어 로드
with open(WORDS_PATH, 'r', encoding='utf-8') as f:
    word_list = set(json.load(f))

with open(ANSWERS_PATH, 'r', encoding='utf-8') as f:
    answer_list = set(json.load(f))

# 정답도 반드시 벡터에 포함
target_words = word_list | answer_list
print(f"추출 대상: {len(target_words)}개 단어")

# vec 파일에서 필요한 단어만 추출
vectors = {}
with io.open(VEC_PATH, 'r', encoding='utf-8', newline='\n', errors='ignore') as f:
    n, d = map(int, f.readline().split())
    print(f"FastText 전체: {n}개 단어, {d}차원")

    for line in f:
        tokens = line.rstrip().split(' ')
        word = tokens[0]
        if word in target_words:
            vectors[word] = [float(x) for x in tokens[1:]]
            if len(vectors) % 100 == 0:
                print(f"  {len(vectors)}개 추출됨...")
        if len(vectors) == len(target_words):
            break

# 벡터를 못 찾은 단어 확인
missing = target_words - set(vectors.keys())
if missing:
    print(f"\n⚠️ 벡터 없는 단어 {len(missing)}개:")
    for w in sorted(missing):
        print(f"  - {w}")
else:
    print("\n✅ 모든 단어의 벡터를 찾았습니다.")

# 저장
with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(vectors, f, ensure_ascii=False)

print(f"\n완료! {len(vectors)}개 단어 벡터 → {OUTPUT_PATH}")
print(f"파일 크기: 약 {os.path.getsize(OUTPUT_PATH) / 1024 / 1024:.1f}MB")
