from pydantic import BaseModel


class InferRequest(BaseModel):
    image_data: str
    image_id: str
