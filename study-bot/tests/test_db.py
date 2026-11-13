import pytest

import db


@pytest.fixture
async def path(tmp_path):
    p = str(tmp_path / "test.db")
    await db.init_db(p)
    return p


async def test_add_and_list(path):
    await db.add_task(1, 42, "Write README", path=path)
    rows = await db.list_tasks(1, path=path)
    assert len(rows) == 1
    assert rows[0][2] == "Write README"


async def test_tasks_are_per_server(path):
    await db.add_task(1, 42, "Server one task", path=path)
    assert await db.list_tasks(2, path=path) == []


async def test_complete_task(path):
    tid = await db.add_task(1, 42, "Study", path=path)
    assert await db.complete_task(1, tid, path=path) is True
    assert await db.list_tasks(1, path=path) == []
    assert len(await db.list_tasks(1, include_done=True, path=path)) == 1
    # completing again, or from another server, fails
    assert await db.complete_task(1, tid, path=path) is False
    assert await db.complete_task(2, tid, path=path) is False
