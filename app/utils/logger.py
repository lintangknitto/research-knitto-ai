from app.config.meilisearch_client import meiliClient


async def write_log(
    id: str,
    question: str,
    answer: str,
    response_time: int,
    intent: str,
    context: str,
    nohp: str,
    level: str,
    usage_metadata: object,
    date: int,
):
    log_data = {
        "id": id,
        "question": question,
        "answer": answer,
        "response_time": response_time,
        "intent": intent,
        "context": context,
        "nohp": nohp,
        "level": level,
        "usage_token": usage_metadata,
        "kesesuaian": "false",
        "date": date,
    }

    index = meiliClient.index("log_chatbot")
    index.add_documents([log_data])
