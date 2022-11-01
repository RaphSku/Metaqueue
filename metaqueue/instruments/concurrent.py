"""
TaskRunner
----------
Concurrently run coroutines as tasks
"""

import asyncio 
from typing import Any, Callable


class TaskRunner:
    """
    TaskRunner is a utility class helping running
    coroutines concurrently
    """

    def __init__(self) -> None:
        pass


    @staticmethod
    async def run(async_funcs: list[Callable], args: list[Any]):
        """
        From the coroutines, tasks will be created and run concurrently

        Parameters
        ----------
        async_funcs: list[Callable]
            A list of coroutines, async functions
        args: list[Any]
            The arguments of the coroutines which should be passed to them

        Returns
        -------
        list
            The result of the awaitables are returned in order as the awaitables
            were given as input
        """
        tasks = []
        for async_func, arg in zip(async_funcs, args):
            tasks.append(asyncio.create_task(async_func(*arg)))

        return await asyncio.gather(*tasks)
        