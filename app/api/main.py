from fastapi import FastAPI
from pydantic import BaseModel
from app.services.generate_answer import generate_answer
import uuid

app = FastAPI()


class Chat(BaseModel):
    nama_customer: str
    question: str
    no_hp: str
    first: bool


@app.post("/chat/")
async def chat(item: Chat):
    id_log = str(uuid.uuid4())
    response = await generate_answer(
        id_log=id_log,
        question=item.question,
        first=item.first,
        nohp=item.no_hp,
        nama_customer=item.nama_customer,
    )
    return {"id_log": id_log, "answer": response}
