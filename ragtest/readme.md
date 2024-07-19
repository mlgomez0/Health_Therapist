python3 -m graphrag.index --init --root ./ragtest

cd ragtest , vi settings

sudo find / -name openai_embeddings_llm.py


python3 -m graphrag.index --root ./ragtest

python3 -m graphrag.query --root ./ragtest --method global "Who is Fahd Mirza?"