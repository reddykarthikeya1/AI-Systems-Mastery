# Debug Lab: Module 13 — FastAPI Traps

## How to Run
```bash
python debug_lab/broken_catalog_api.py
```

## Observed Symptoms
1. **Route shadowing**:
   `GET /items/special` returns `{"item_id": "special", "type": "dynamic"}` instead of invoking `get_special_item()`.
2. **ASGI event loop thread blocking**:
   `async def` route calling `time.sleep()` freezes all concurrent requests served by that worker process.
