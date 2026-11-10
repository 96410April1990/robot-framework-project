from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

expected = "The refund will arrive within 5 business days."
actual = "You should receive your money within one working week."

expected_embedding = model.encode([expected])
actual_embedding = model.encode([expected])

similarity = cosine_similarity(
    expected_embedding,
    actual_embedding
)[0][0]

print("Similarity:", similarity)

assert similarity > 0.70
