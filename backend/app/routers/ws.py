
from fastapi import APIRouter, WebSocket, Query
from typing import List
import json
from ..services.pubsub import get_redis
router = APIRouter(tags=["ws"])
@router.websocket("/ws/subscribe")
async def ws_subscribe(ws: WebSocket, channels: List[str] = Query(default=[])):
    await ws.accept()
    if not channels:
        await ws.send_json({"error":"no_channels"}); await ws.close(); return
    r = get_redis(); ps = r.pubsub()
    await ps.subscribe(*channels)
    try:
        async for m in ps.listen():
            if m and m.get("type")=="message":
                data = m.get("data")
                try: payload = json.loads(data)
                except: payload = {"raw": data}
                await ws.send_json({"channel": m["channel"], "data": payload})
    finally:
        await ps.close(); await ws.close()
