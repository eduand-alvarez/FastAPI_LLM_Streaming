import uvicorn
import os
import requests
import asyncio
import logging
import warnings

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from queue import Queue

from utils.payloads import InferencePayload
from utils.streamer import CustomStreamer
from utils.loader import ITREXLoader
from utils.generation import start_generation

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore")

# Creating the queue, streamers, models, and tokenizers

# neural_chat_7B_v1_1
logger.info("loading Intel/neural-chat-7b-v1-1")
neural_chat_7B_v1_1_Model, neural_chat_7B_v1_1_Tokenizer = ITREXLoader('Intel/neural-chat-7b-v1-1')

# neural_chat_7B_v3_1
#logger.info("loading Intel/neural-chat-7b-v3-1")
#neural_chat_7B_v3_1_streamer_queue = Queue()
#neural_chat_7B_v3_1_Model, neural_chat_7B_v3_1_Tokenizer = ITREXLoader('Intel/neural-chat-7b-v3-1')

#neural_chat_7B_v3_0_Model, neural_chat_7B_v3_0_Tokenizer = ITREXLoader('Intel/neural-chat-7b-v3')
#neural_chat_7B_v3_2_Model, neural_chat_7B_v3_2_Tokenizer = ITREXLoader('Intel/neural-chat-7b-v3-2')



# Generation initiator and response server
async def response_generator(query, model, tokenizer, streamer, streamer_queue):

    start_generation(query, model, tokenizer, streamer)

    while True:
        value = streamer_queue.get()
        if value == None:
            break
        yield value
        streamer_queue.task_done()
        await asyncio.sleep(0.1)


@app.get("/ping")
async def ping():
    """Ping server to determine status

    Returns
    -------
    API response
        response from server on health status
    """
    return {"message":"Server is Running"}


@app.get('/query-stream/')
async def stream(payload:InferencePayload):
    print(f'Query receieved: {payload.query}')
    
    model = payload.selected_model
    
    if model == 'Intel/neural-chat-7b-v1-1':
        logger.info("Intel/neural-chat-7b-v1-1 selected for inference")
        neural_chat_7B_v1_1_streamer_queue = Queue()
        neural_chat_7B_v1_1_Streamer = CustomStreamer(neural_chat_7B_v1_1_streamer_queue, neural_chat_7B_v1_1_Tokenizer, True)
        return StreamingResponse(response_generator(payload.query, neural_chat_7B_v1_1_Model, 
                                                    neural_chat_7B_v1_1_Tokenizer, neural_chat_7B_v1_1_Streamer, 
                                                    neural_chat_7B_v1_1_streamer_queue), media_type='text/event-stream')
    #elif model == 'Intel/neural-chat-7b-v3-1':
    #    logger.info("Intel/neural-chat-7b-v3-1 selected for inference")
    #    neural_chat_7B_v3_1_Streamer = CustomStreamer(neural_chat_7B_v3_1_streamer_queue, neural_chat_7B_v3_1_Tokenizer, True)
    #    return StreamingResponse(response_generator(payload.query, neural_chat_7B_v3_1_Model, 
    #                                                neural_chat_7B_v3_1_Tokenizer, neural_chat_7B_v3_1_Streamer, 
    #                                                neural_chat_7B_v3_1_streamer_queue), media_type='text/event-stream')

if __name__ == "__main__":
    uvicorn.run("serve:app", host="0.0.0.0", port=8080, log_level="info")