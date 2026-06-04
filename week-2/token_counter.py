""" CLI tool. """

import tiktoken
import sys

file_name = input("Enter file name: ")

try:
    with open(file_name, "r", encoding="utf-8") as file:
        content = file.read()
    if not content.strip():
        print("Error: File is empty.")
        sys.exit(1)

except FileNotFoundError:
    print("File not found")
    sys.exit(1)

print("Select your preferred model-")

MODEL_COSTS = {
    "gpt-5": 1.25,
    "gpt-5-mini": 0.25,
    "gpt-5-nano": 0.05,
    "gpt-4.1": 2.00,
    "gpt-4.1-mini": 0.40,
    "gpt-4.1-nano": 0.10,
    "gpt-4o": 2.50,
    "gpt-3.5-turbo": 0.50,
}

for model, cost in MODEL_COSTS.items():
    print(f"{model} : ${cost}/1M tokens")

model = input("\nPlease enter the model name:- ")

try:
    cost = MODEL_COSTS[model]
except KeyError:
    print(f"'{model}' is not a supported model.")
    sys.exit(1)

enc = tiktoken.encoding_for_model(model)
tokens = enc.encode(content)
token_count = len(tokens)
char_count = len(content)
word_count = len(content.split())
input_cost = (token_count / 1_000_000) * MODEL_COSTS[model]

print("Analysis Results")
print("-" * 20)
print(f"file name      : {file_name}")
print(f"Model Selected : {model}")
print(f"Rate           : ${MODEL_COSTS[model]}/1M tokens")
print(f"Characters     : {char_count}")
print(f"Words          : {word_count}")
print(f"Tokens         : {token_count}")
print(f"Input Cost     : ${input_cost:.7f}")
