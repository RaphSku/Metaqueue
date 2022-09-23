import asyncio 


class TaskRunner:
    def __init__(self) -> None:
        pass


    @staticmethod
    async def run(async_funcs, args):
        tasks = []
        for async_func, arg in zip(async_funcs, args):
            tasks.append(asyncio.create_task(async_func(*arg)))

        return await asyncio.gather(*tasks)
        