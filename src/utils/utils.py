import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Callable

_executor = ThreadPoolExecutor()


async def cpu_bound_task(func: Callable, *args):
    """
    Execute async function in a separate thread, without blocking the main event
    loop.
    """
    return await asyncio.get_event_loop().run_in_executor(_executor, func, *args)
