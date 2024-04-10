from threading import Thread


def start_generation(query, model, tokenizer, streamer):
    
    system_message = "You are assistant that behaves very professionally. You will only provide the answer \
    if you know the answer. If you do not know the answer, you will say I dont know."
    
    template = f"""
    ### System: {system_message} ### User: {query} ### Assistant:
    """
    
    inputs = tokenizer(query, return_tensors="pt").input_ids
    
    # key word arguments that are provided to the model.generate()function
    # Includes, inputs, max_tokens, streamer, temparature
    generation_kwargs = {
        'input_ids': inputs,  # Assuming model.generate expects input_ids
        'streamer': streamer,
        'max_new_tokens': 75,
        'temperature': 0.3
    }
    
    # Starting the thread with the stream
    thread = Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()
    
