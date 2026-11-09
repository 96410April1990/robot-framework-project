from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

expected = "The refund will be processed within 5 business days."
actual = "You should receive your refund within one working week."

e1 = model.encode([expected])
e2 = model.encode([actual])

score = cosine_similarity(e1, e2)[0][0]

print("Similarity:", score)

assert score > 0.70