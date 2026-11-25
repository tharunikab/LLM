from transformers import pipeline

print("*** 1. BERT fill-mask Example ***")
unmasker = pipeline("fill-mask", model="bert-base-uncased")
bert_results = unmasker(
    "The scientist looked through the [MASK] to observe the distant galaxy.",
    top_k=3,
)
for res in bert_results:
  print(f"Prediction: {res['token_str']:<12} | Score: {res['score']:.4f}")

print("\n*** 2. GPT-2 text-generation Example ***")
generator = pipeline("text-generation", model="gpt2")
gpt_result = generator(
    "Artificial intelligence is transforming healthcare by",
    max_new_tokens=25,
    num_return_sequences=1,
    pad_token_id=50256,
)
print("Generated Text:\n", gpt_result[0]["generated_text"])
#why word order would be lost without positional encoding:
#1. Unlike older models that read one word at a time, Transformers process all words in a sentence simultaneously in parallel.
#2. Self-attention compares every word to every other word using dot products, an operation that is completely order-blind.
#3. Without position data, "The dog chased the cat" and "The cat chased the dog" would look identical to the model.
#4. Positional encoding adds a unique numerical signal to each word vector so the model knows its exact place in the sequence.