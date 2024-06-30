from pydantic import BaseModel


class JWTPayload(BaseModel):
    sub: str
    t: str
    p: str
