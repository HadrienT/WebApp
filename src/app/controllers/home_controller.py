import base64
import multiprocessing
from datetime import datetime
from typing import Any, Optional
from bson import ObjectId

from fastapi import File, Request, UploadFile
from fastapi.responses import JSONResponse

from controllers import user_controller
from config.templates import templates
from config.database import get_collection
from models import image_model, user_model
from MachineLearning import Infer


def get_all_user_images(user_id: str) -> list[image_model.ImageResponse]:
    cursor = get_collection('images').find({"user_id": user_id})
    images = [image for image in cursor]
    for image in images:
        image["_id"] = str(image["_id"])  # Convert the _id field to a string
        image["description"] = image.get("description", None)  # Set a default value for description if it's missing
        # Convert the creation_date field to a string in ISO 8601 format
        if "creation_date" in image:
            image["creation_date"] = image["creation_date"].isoformat()
        else:
            image["creation_date"] = None
        image["image_data"] = base64.b64encode(image["image_data"]).decode("utf-8")  # Encode the image data

    return images


async def get_images(current_user: user_model.User) -> list[image_model.ImageResponse]:
    images = get_all_user_images(str(current_user["_id"]))
    return images


async def upload_image(file: UploadFile = File(...), current_user: user_model.User = None) -> JSONResponse:
    memory = await user_controller.get_user_memory_usage(current_user)
    if memory["memory_usage"] + file.size > memory["max_memory_allowed"]:
        return JSONResponse(content={"error": "Storage limit exceeded"}, status_code=400)

    # Read the uploaded file
    contents = await file.read()

    # Calculate the file size in bytes
    file_size = len(contents)

    # Create a new Image object using the provided data
    new_image = image_model.Image(
        user_id=str(current_user["_id"]),
        image_data=contents,
        creation_date=datetime.utcnow(),
        file_size=file_size,
    )

    # Insert the new image into the MongoDB collection
    result = get_collection("images").insert_one(new_image.dict())

    # Return the inserted image ID
    return JSONResponse(content={"image_id": str(result.inserted_id)})


async def show_account(request: Request, current_user: user_model.User) -> templates.TemplateResponse:
    user_info = {
        "username": current_user["username"],
        "email": current_user["email"],
        "balance": current_user["balance"],
    }
    return templates.TemplateResponse("myaccount.html", {"request": request, "user_info": user_info})


def set_image_description(image_id: str, description: str) -> Optional[dict]:
    collection = get_collection('images')  # Replace with your collection name

    result = collection.update_one({"_id": ObjectId(image_id)}, {"$set": {"description": description}})
    if result.modified_count > 0:
        return {"image_id": image_id, "description": description}
    else:
        return None


async def process_image_data(image_data: str, image_id: str) -> Any:
    # Remove the data URL prefix
    image_data = image_data.split(",")[1]

    # Decode the base64 encoded image data
    image_bytes = base64.b64decode(image_data)

    # Create a multiprocessing Queue object
    queue: multiprocessing.Queue[Any] = multiprocessing.Queue()

    # Start the second process
    p2 = multiprocessing.Process(target=Infer.main, args=(queue, image_bytes))
    p2.start()

    # Wait for the second process to finish
    p2.join()

    # Get the result from the Queue
    description = queue.get()
    # Update the image description in the database
    set_image_description(image_id, description[0])

    return {"description": description[0]}


async def delete_image(image_id: str, current_user: user_model.User) -> JSONResponse:
    # Delete the image from the database
    result = get_collection("images").delete_one({"_id": ObjectId(image_id), "user_id": str(current_user["_id"])})
    # Return the result of the deletion
    return JSONResponse(content={"deleted_count": result.deleted_count})
