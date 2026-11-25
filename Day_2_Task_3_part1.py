import matplotlib.pyplot as plt
import numpy as np


def get_positional_encoding(max_pos, d_model):
  PE = np.zeros((max_pos, d_model))
  positions = np.arange(max_pos)[:, np.newaxis] 
  div_term = np.exp(
      np.arange(0, d_model, 2) * -(np.log(10000.0) / d_model)
  ) 

  PE[:, 0::2] = np.sin(positions * div_term)  
  PE[:, 1::2] = np.cos(positions * div_term)  
  return PE


pe_matrix = get_positional_encoding(max_pos=10, d_model=8)

plt.figure(figsize=(8, 5))
plt.imshow(pe_matrix, cmap="coolwarm", aspect="auto")
plt.colorbar(label="Encoding Value")
plt.title("Sinusoidal Positional Encoding (10 Positions x 8 Dimensions)")
plt.xlabel("Embedding Dimension (i)")
plt.ylabel("Token Position (pos)")
plt.xticks(range(8))
plt.yticks(range(10))
plt.tight_layout()
plt.savefig("positional_encoding_heatmap.png", dpi=150)
plt.show()
