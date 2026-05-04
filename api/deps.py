from fastapi import Header, HTTPException
from config import config

CFG = config()


def require_scheduler_token(access_token: str = Header(default="", alias="Access-Token")) -> None:
    if not access_token or access_token != CFG.SCHEDULER_ACCESS_TOKEN:
        raise HTTPException(status_code=403, detail="Access denied")
