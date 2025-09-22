from transformers import pipeline

gen = pipeline("text-generation",model="gpt2")
result = gen("once upon a time", max_length = 30, num_return_sequences = 1)
print(result)