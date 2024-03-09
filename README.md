# FastAPI_LLM_Streaming

This repository provides the necessary tools to deploy streaming inference endpoints for large language models (LLMs) hosted on Hugging Face, using FastAPI. It leverages the power of Hugging Face models and Intel's optimization libraries to offer efficient and scalable real-time inference capabilities.

## Overview

The project includes a Python script (`serve.py`) for setting up a FastAPI server that can handle streaming requests to LLMs, providing an efficient way to interact with models for real-time inference. It's optimized for Intel hardware, utilizing the `intel_extension_for_transformers` library to enhance performance on compatible CPUs.

## Installation

To get started, clone this repository and install the required dependencies.

```bash
git clone https://github.com/yourusername/your-repository-name.git
cd your-repository-name
pip install -r requirements.txt
```

## Usage
1. Start the FastAPI server:

Run the serve.py script to start the server:

```bash
python serve.py
```
This command starts the FastAPI application on port 5004, making it accessible on your network.

2. Interacting with the API:

Once the server is running, you can make HTTP GET requests to the /query-stream/ endpoint to interact with the deployed LLM. The request should include the query parameter and the selected_model parameter to specify the model you wish to use for inference.

Example using curl:

```bash
curl "http://localhost:5004/query-stream/?query=Hello%20world&selected_model=Intel/neural-chat-7b-v1-1"
```

## Supported Models
Currently, the server is configured to support specific models from Hugging Face. These models are defined within the serve.py script and can be easily extended by modifying the ITREXLoader function within loader.py.


