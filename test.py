"""
use embeddings to encode words or sentences.

Run flm serve gemma3:4b --embed 1 in a command shell before
"""


from openai import OpenAI
import numpy as np

client = OpenAI(
    base_url="http://127.0.0.1:52625/v1",
    api_key="flm"
)

text1 = ["A dog is running"]
text1b = ["A dog is sleeping"]
text2 = ["A cat is sleeping"]
text3 = ["The stock market crashed"]

emb1 = client.embeddings.create(
    model="embed-gemma",
    input=text1
)

emb1b = client.embeddings.create(
    model="embed-gemma",
    input=text1b
)

emb2 = client.embeddings.create(
    model="embed-gemma",
    input=text2
)

emb3 = client.embeddings.create(
    model="embed-gemma",
    input=text3
)

# Extract vectors
vectors = [
    np.array(emb1.data[0].embedding),
    np.array(emb1b.data[0].embedding),
    np.array(emb2.data[0].embedding),
    np.array(emb3.data[0].embedding)
]

# Normalize vectors
norms = [np.linalg.norm(v) for v in vectors]
print(f"Vector norms: {norms}")

# Compute cosine similarity matrix correctly
n = len(vectors)
cosine_matrix = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        cosine_matrix[i, j] = np.dot(vectors[i], vectors[j]) / (norms[i] * norms[j])

print("Cosine Similarity Matrix (diagonal should be 1):")
print(cosine_matrix)