import numpy as np

np.random.seed(0)
X = np.random.randn(4, 3)
Wq = np.random.randn(3, 3)
Wk = np.random.randn(3, 3)
Wv = np.random.randn(3, 3)

Q = X @ Wq
K = X @ Wk
V = X @ Wv

d = K.shape[-1]
scores = (Q @ K.T) / np.sqrt(d)

def softmax(x):
  exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
  return exp_x / np.sum(exp_x, axis=-1, keepdims=True)


attention_weights = softmax(scores)

output = attention_weights @ V

print("Attention Weight Matrix (4x4):")
print(np.round(attention_weights, 4))

row_sums = np.sum(attention_weights, axis=1)
print("\nRow Sums:", row_sums)
assert np.allclose(row_sums, 1.0), "Rows do not sum to 1!"
print("Verification passed: Each row sums to 1.")

# Query, Key, and Value:

#1. Imagine typing a Query (Q) into a search engine to find information on a specific topic.
#2. The search engine compares your query against the Keys (K)—the titles, tags, and keywords indexed for every webpage.
#3. Matching your query with each key produces a relevance score showing how closely each page fits what you want.
#4. Softmax converts those scores into percentage weights so the best-matching pages get the highest focus.
#5. Finally, you read the Values (V)—the actual content inside those pages—blended together according to their relevance weights.
