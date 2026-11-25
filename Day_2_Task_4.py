import time
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

torch.manual_seed(42)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def create_dataset(num_samples=5000, seq_len=8, vocab_size=20):
  X = torch.randint(0, vocab_size, (num_samples, seq_len))
  half = num_samples // 2
  X[:half], _ = torch.sort(X[:half], dim=1)
  perm = torch.randperm(num_samples)
  X = X[perm]
  y = (X[:, 1:] >= X[:, :-1]).all(dim=1).long()
  return X, y

X_train, y_train = create_dataset(5000)
X_test, y_test = create_dataset(1000)

train_loader = DataLoader(
    TensorDataset(X_train, y_train), batch_size=64, shuffle=True
)
test_loader = DataLoader(TensorDataset(X_test, y_test), batch_size=64)

class TinyLSTM(nn.Module):

  def __init__(self, vocab_size=20, d_model=32, num_layers=2):
    super().__init__()
    self.embed = nn.Embedding(vocab_size, d_model)
    self.lstm = nn.LSTM(
        d_model, d_model, num_layers=num_layers, batch_first=True
    )
    self.fc = nn.Linear(d_model, 2)

  def forward(self, x):
    x = self.embed(x)
    out, _ = self.lstm(x)
    return self.fc(out[:, -1, :]) 

class TinyTransformer(nn.Module):

  def __init__(self, vocab_size=20, d_model=32, seq_len=8, num_layers=2):
    super().__init__()
    self.embed = nn.Embedding(vocab_size, d_model)
    self.pos_embed = nn.Parameter(torch.randn(1, seq_len, d_model))
    encoder_layer = nn.TransformerEncoderLayer(
        d_model=d_model, nhead=4, dim_feedforward=64, batch_first=True
    )
    self.transformer = nn.TransformerEncoder(
        encoder_layer, num_layers=num_layers
    )
    self.fc = nn.Linear(d_model, 2)

  def forward(self, x):
    x = self.embed(x) + self.pos_embed
    out = self.transformer(x)
    return self.fc(out.mean(dim=1))  # Mean pooling across sequence

def train_and_evaluate(model, name, epochs=12):
  model.to(device)
  optimizer = torch.optim.Adam(model.parameters(), lr=0.003)
  criterion = nn.CrossEntropyLoss()

  start_time = time.time()
  model.train()
  for epoch in range(epochs):
    for bx, by in train_loader:
      bx, by = bx.to(device), by.to(device)
      optimizer.zero_grad()
      loss = criterion(model(bx), by)
      loss.backward()
      optimizer.step()
  train_time = time.time() - start_time

  model.eval()
  correct, total = 0, 0
  with torch.no_grad():
    for bx, by in test_loader:
      bx, by = bx.to(device), by.to(device)
      preds = model(bx).argmax(dim=1)
      correct += (preds == by).sum().item()
      total += by.size(0)

  acc = (correct / total) * 100
  print(f"{name:<22} | Accuracy: {acc:.2f}% | Training Time: {train_time:.3f}s")
  return acc, train_time


print("*** Model Comparison *** ")
train_and_evaluate(TinyLSTM(), "2-Layer LSTM")
train_and_evaluate(TinyTransformer(), "2-Layer Transformer")

#Reasons transformers replaced RNNs:
#1. Parallelism: RNNs must process text sequentially one word at a time, whereas Transformers process every word in a sequence simultaneously, making training dramatically faster on modern GPUs.
#2. Long-Range Attention: Self-attention connects any two words directly in a single step regardless of distance, eliminating the information bottleneck RNNs suffer over long paragraphs.
#3. Scaling: Transformer performance improves predictably as you increase model parameters, dataset size, and compute, whereas RNNs plateau much earlier.
#4. Transfer Learning: Transformers pre-trained on massive unlabeled text corpora (like BERT and GPT) learn general language representations that can be easily fine-tuned for downstream tasks with minimal data.

#Vanishing gradient problem:
#1. During training, neural networks update their weights by propagating error signals (gradients) backward from the end of a sequence to the beginning.
#2. In RNNs, this requires multiplying the same weight matrix repeatedly across every time step in the sequence.
#3. If those numbers are smaller than 1, multiplying them repeatedly causes the gradient to shrink exponentially until it approaches zero.
#4. As a result, early layers stop updating their weights, and the network fails to learn connections between distant words.


#Explaination of how ChatGPT-style models generate:
#1.When you type a request, the model does not look up a pre-written answer in a database. 
#2.Instead, it reads your entire message at once, pays close attention to how every word relates to the others, and calculates the odds of what the single best next word—or word fragment, called a "token"—should be.
#3.Once it selects that token, it attaches it to your original prompt, re-reads the entire updated text, and predicts the next token after that. 
#4.It repeats this rapid loop dozens of times per second until it completes a full, coherent response. 
#5.Because it constantly re-evaluates the entire conversation at every step, the final output sounds remarkably natural and context-aware.