"""
TestTaskRunner
--------------
Testing whether the taskrunner returns the results in the expected order
and if multiple tasks can be processed with their arguments without problems
"""

import pytest
import asyncio

from metaqueue.instruments import TaskRunner


async def task(a, b):
    await asyncio.sleep(1)
    return a * b


class TestTaskRunner:
    @pytest.mark.asyncio
    async def test_runner_s01(self):
        results = await TaskRunner.run(async_funcs = [task, task], args = [(2, 5), (5, 10)])

        assert results == [10, 50]