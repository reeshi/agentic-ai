import tiktoken

# Get's encoding of the gpt-4 model
enc = tiktoken.encoding_for_model("gpt-4")

# text we want to encode into to tokens
text = "Hey, there my name is rishikesh yadav"
tokens = enc.encode(text)
print("Tokens : ", tokens)

# decode back from tokens to english
decoded = enc.decode(tokens)
print("Decoded : ", decoded)
