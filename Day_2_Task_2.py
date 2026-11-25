import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer

print("*** 1.MULTI-HEAD ATTENTION FROM SCRATCH ***")
np.random.seed(42)

X = np.random.randn(4, 4)
Wq = np.random.randn(4, 4)
Wk = np.random.randn(4, 4)
Wv = np.random.randn(4, 4)
Wo = np.random.randn(4, 4)

Q, K, V = X @ Wq, X @ Wk, X @ Wv


def softmax(x):
  exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
  return exp_x / np.sum(exp_x, axis=-1, keepdims=True)


def attention(q, k, v):
  scores = (q @ k.T) / np.sqrt(q.shape[-1])
  weights = softmax(scores)
  return weights @ v

Q_heads = np.split(Q, 2, axis=-1)
K_heads = np.split(K, 2, axis=-1)
V_heads = np.split(V, 2, axis=-1)

head_1 = attention(Q_heads[0], K_heads[0], V_heads[0])
head_2 = attention(Q_heads[1], K_heads[1], V_heads[1])

concat = np.concatenate([head_1, head_2], axis=-1)
final_output = concat @ Wo

print("Head 1 shape:", head_1.shape)
print("Head 2 shape:", head_2.shape)
print("Concatenated shape:", concat.shape)
print("Final Output:\n", np.round(final_output, 4))

print("\n***2: HUGGING FACE ATTENTION INSPECTION ***")
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased", output_attentions=True)

sentence = "The bank by the river was steep"
inputs = tokenizer(sentence, return_tensors="pt")
tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

with torch.no_grad():
  outputs = model(**inputs)

attention_matrix = outputs.attentions[0][0, 0]
bank_index = tokens.index("bank")
bank_scores = attention_matrix[bank_index]

print(f"Tokens: {tokens}\n")
print("How much 'bank' pays attention to each word (Layer 0, Head 0):")
for word, score in zip(tokens, bank_scores):
  print(f"  {word:<10}: {score.item():.4f}")

# Why Several Heads Are Better Than One

#1. A single attention head averages all relationships together, forcing the model to compromise on which words to focus on.
#2. Multiple heads allow the model to attend to different types of information simultaneously across separate representation subspaces.
#3. For example, one head can track syntactic grammar (such as subject-verb agreement) while another resolves word sense (linking "bank" to "river" rather than finance).
#4. Combining these specialized perspectives gives the model a much richer, multi-layered understanding of context.
