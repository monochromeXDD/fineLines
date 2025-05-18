#Temperature: a hyperparameter that controls the randomness of the generated text. It essentially adjusts the probability distribution of the next word predicted by the model, influencing whether the output is more predictable or creative. 
#Lower Temp(0.0 - 0.4): Makes the output more deterministic and focused. 
#Higher Temp(0.8 - 1.0): Increases randomness and creativity.
#Medium Temp(0.5 - 0.7): Balances randomness and determinism, offering a good starting point for general purposes. 


from langchain_ollama import ChatOllama
llm = ChatOllama(
    model = "gemma3:4b-it-qat",
    temperature = 0.2 #
)