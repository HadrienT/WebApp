import io
from PIL import Image, UnidentifiedImageError
from torch.utils.data import Dataset
from typing import Any, Union
import torch.types
from torchvision import transforms


class CustomDataset(Dataset[Any]):
    def __init__(self, image_bytes: bytes, transform: transforms.Compose = None) -> None:
        self.image_bytes = image_bytes
        self.transform = transform

    def __len__(self) -> int:
        return 1  # Since we're using a single image

    def __getitem__(self, idx: int) -> Union[torch.Tensor, Image.Image]:
        if idx >= self.__len__():
            raise IndexError("Index out of bounds")

        try:
            image = Image.open(io.BytesIO(self.image_bytes))
        except UnidentifiedImageError:
            # Return a placeholder image or handle the problematic image in another way
            image = Image.new('RGB', (224, 224), color='gray')

        if self.transform:
            image = self.transform(image)

        return image
