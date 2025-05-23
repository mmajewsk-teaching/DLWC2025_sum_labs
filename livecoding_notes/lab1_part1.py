# %% [markdown]
# # Lab 1: Building a Basic RAG System
# 
# In this lab, we'll create a simple Retrieval Augmented Generation (RAG) system using PyTorch and Hugging Face models.

# %% [markdown]
# ## Setup
# First, let's import the necessary libraries and set up our environment.

# %%
# Standard library imports
import os
import time

# %%
# Third-party imports
import torch
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from transformers import AutoTokenizer, AutoModel

# %%
# Check if CUDA is available and set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# %% [markdown]
# ## Download and Load Language Model
# 
# We'll use a pre-trained language model from Hugging Face for generating embeddings.

# %%
# Define which model to use - we'll use a small but effective model
model_name = "sentence-transformers/all-MiniLM-L6-v2"
print(f"We'll use the model: {model_name}")

# %%
# Load the tokenizer - this converts text to tokens the model can understand
tokenizer = AutoTokenizer.from_pretrained(model_name)
print(f"Tokenizer loaded with vocabulary size: {len(tokenizer)}")

# %%
# Let's see how the tokenizer works with a simple example
example_text = "Hello, this is a sample text for our RAG system!"
tokens = tokenizer(example_text)
print("Input text:", example_text)
print("Token IDs:", tokens["input_ids"])
print("Decoded tokens:", tokenizer.convert_ids_to_tokens(tokens["input_ids"]))

# %%
# Now load the actual model
model = AutoModel.from_pretrained(model_name).to(device)
print(f"Model loaded successfully with {sum(p.numel() for p in model.parameters())} parameters")

# %% [markdown]
# ## Generate Embeddings
# 
# Now we'll see how to generate embeddings for text. Embeddings are vector representations that capture semantic meaning.

# %%
# First, prepare text for the model by tokenizing it
text_to_embed = "This is a sample text to demonstrate embedding generation."
encoded_input = tokenizer(text_to_embed, padding=True, truncation=True, return_tensors="pt").to(device)
print("Encoded input shape:")
for key, value in encoded_input.items():
    print(f"  {key}: {value.shape}")

# %%
# Pass the encoded input through the model
with torch.no_grad():
    model_output = model(**encoded_input)

# Look at the model output
print("Model output keys:", model_output.keys())
print("Last hidden state shape:", model_output.last_hidden_state.shape)
# This is a 3D tensor: [batch_size, sequence_length, hidden_size]

# %%
# To get a single vector for the entire text, we'll use mean pooling
# Since we're only processing a single sentence without batching,
# we can simply take the mean of the token embeddings
token_embeddings = model_output.last_hidden_state

# %%
# Calculate mean across the sequence dimension (dim=1)
final_embedding = torch.mean(token_embeddings, dim=1).squeeze()
print("Final embedding shape:", final_embedding.shape)

# Convert to numpy array for easier handling
embedding = final_embedding.cpu().numpy()
print("Embedding numpy shape:", embedding.shape)
print("First 5 values:", embedding[:5])