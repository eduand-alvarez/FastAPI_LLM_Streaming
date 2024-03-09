from pydantic import BaseModel

class InferencePayload(BaseModel):
    query: str
    selected_model: str