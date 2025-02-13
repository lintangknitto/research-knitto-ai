from fastapi import APIRouter

import_router = APIRouter()

@import_router.post("/import")
async def import_data():
    """
    Endpoint untuk mengimpor data stok dari MySQL ke MeiliSearch dengan vektor embedding.
    """
    return {"result": "oke"}
