from datetime import timedelta
import os
import dotenv


def load_config() -> dict[str, str]:
    dotenv.load_dotenv()
    config = {
        "JWT_SECRET": os.getenv("JWT_SECRET"),
        "JWT_ALGORITHM": os.getenv("JWT_ALGORITHM"),
        "JWT_EXPIRATION": timedelta(minutes=int(os.getenv("JWT_EXPIRATION"))),
    }
    return config
