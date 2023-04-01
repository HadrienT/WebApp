from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from datetime import datetime


class Image(BaseModel):
    _id: Optional[ObjectId] = Field(alias="_id")
    user_id: str
    image_data: bytes
    description: Optional[str] = None
    creation_date: datetime
    file_size: int

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat(),
        }


class ImageResponse(BaseModel):
    id: str = Field(..., alias="_id")  # Add this line
    user_id: str
    description: Optional[str] = None  # Set the default value to None
    image_data: str
    creation_date: datetime = None  # Set the default value to None

    class Config:
        json_encoders = {
            ObjectId: str
        }
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "_id": "60ba32f0272e7d5f72ce5bc7",
                "user_id": "609a9e8e272e7d5f72ce5b7c",
                "description": "A beautiful sunset",
                "image_data": "base64_encoded_image_data",
                "creation_date": "2023-03-22T08:12:00",
            }
        }
