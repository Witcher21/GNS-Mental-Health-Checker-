import asyncio
import traceback
import sys
from nlp_service import process_chat_message

async def run():
    with open("test_out.txt", "w") as f:
        sys.stdout = f
        sys.stderr = f
        try:
            print("Starting test")
            res = await process_chat_message("hi", None)
            print("RES:", res)
        except Exception as e:
            print("FATAL:")
            traceback.print_exc()

asyncio.run(run())
