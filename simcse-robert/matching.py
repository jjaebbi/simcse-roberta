import pyodbc
from transformers import AutoModel, AutoTokenizer
import torch
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

# ... (calculate_similarity, get_highest_similarity_score 함수 정의)
def calculate_similarity(model, tokenizer, text1, text2):
    inputs = tokenizer([text1, text2], return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        similarity_scores = torch.nn.functional.cosine_similarity(outputs.last_hidden_state[0], outputs.last_hidden_state[1], dim=1)
        similarity_score = similarity_scores.mean()  # 여러 점수의 평균을 계산
    return similarity_score



def calculate_max_similarity_per_sentence(model, tokenizer, intro_text, job_posting_text):
    intro_sentences = sent_tokenize(intro_text)
    job_posting_sentences = sent_tokenize(job_posting_text)

    max_scores = []
    for intro_sentence in intro_sentences:
        sentence_scores = [
            calculate_similarity(model, tokenizer, intro_sentence, job_posting_sentence).item()
            for job_posting_sentence in job_posting_sentences
        ]
        max_scores.append(max(sentence_scores))

    return sum(max_scores) / len(max_scores) if max_scores else 0
# 데이터베이스 연결
db = pyodbc.connect('DSN=aws_test_t6;UID=DAJOBA;PWD=DAJOBA')
cursor = db.cursor()

# 트랜스포머 모델 및 토크나이저 초기화
model_path = "kazma1/simcse-robertsmall-matching"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModel.from_pretrained(model_path)






while True:
    cursor.execute("SELECT USER_ID, INTRO_ID, DESIRE_FIELD, INTRO_CONTENT FROM SELF_INTRODUCTION WHERE SIGNAL = 1")
    row = cursor.fetchone()

    if row is None:
        print("All signals processed.")
        break

    intro_id = row[1]
    desire_field = row[2]
    intro_content = row[3]

    # 해당 희망분야의 채용공고 불러오기
    cursor.execute("SELECT JOB_POSTING_ID, TITLE, GROUP_INTRO, MAINDUTIES, QUALIFICATION, PREFERENTIAL FROM JOB_POSTING WHERE JOB_GROUP = ?", desire_field)
    job_postings = cursor.fetchall()

    # 매칭 점수 계산
    scores = []
    for posting in job_postings:
        job_posting_id = posting[0]
        job_posting_content = ' '.join(posting[1:])

        max_similarity_score = calculate_max_similarity_per_sentence(model, tokenizer, intro_content,
                                                                     job_posting_content)
        scores.append((job_posting_id, max_similarity_score))

    # 상위 5개 채용공고 선택
    top_5_postings = sorted(scores, key=lambda x: x[1], reverse=True)[:5]

    # MATCH 테이블에 결과 저장
    for job_posting_id, score in top_5_postings:
        cursor.execute("INSERT INTO MATCH (INTRO_ID, JOB_POSTINGID, MATCH-SCORE) VALUES (?, ?, ?)", (intro_id, job_posting_id, score))
        db.commit()

    # SIGNAL 값을 0으로 업데이트
    cursor.execute("UPDATE SELF_INTRODUCTION SET SIGNAL = 0 WHERE INTRO_ID = ?", intro_id)
    db.commit()

print("Matching results saved to the MATCH table")
