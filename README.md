#roberta-simcse
자기소개서+채용공고 도메인학습후
#simcse-roberta-matching
dev_train.csv 자기소개서  채용공고 스코어 형태의 유사도비교 데이터학습
#검증데이터 
dev.csv  자기소개서 채용공고 스코어 형태의 유사도 데이터

| Model                      | Cosine Pearson | Cosine Spearman | Euclidean Pearson | Euclidean Spearman | Manhattan Pearson | Manhattan Spearman | Dot Pearson | Dot Spearman |
|----------------------------|----------------|-----------------|-------------------|--------------------|-------------------|--------------------|-------------|--------------|
| SimCSE-RoBERTalarge-matching            | 61.23          | 54.12           | 53.37             | 53.32              | 63.14             | 61.82              | 52.14       | 51.33        |
| SimCSE-RoBERTasmall-matching  | 53.12          | 53.09           | 52.31             | 53.24              | 52.81             | 53.65              | 48.08       | 48.35        |
