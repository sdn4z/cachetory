from datetime import datetime, timedelta, timezone

from pytest import mark, raises, fixture
from freezegun import freeze_time

from cachetory.backends.async_.memory import AsyncMemoryBackend


@fixture
async def backend() -> AsyncMemoryBackend[int]:
    return AsyncMemoryBackend[int]()


@mark.asyncio
async def test_get_item_existing(backend: AsyncMemoryBackend[int]):
    await backend.set("foo", 42)
    assert await backend.get("foo") == 42


@mark.asyncio
async def test_get_item_missing(backend: AsyncMemoryBackend[int]):
    assert await backend.get("foo") is None


@mark.asyncio
async def test_set_default(backend: AsyncMemoryBackend[int]):
    await backend.set_default("foo", 42)
    await backend.set_default("foo", 43)
    assert await backend.get("foo") == 42
    assert backend.size == 1


@mark.asyncio
async def test_delete_existing(backend: AsyncMemoryBackend[int]):
    await backend.set("foo", 42)
    assert await backend.delete("foo")


@mark.asyncio
async def test_delete_missing(backend: AsyncMemoryBackend[int]):
    assert not await backend.delete("foo")


@mark.asyncio
async def test_set_get_many(backend: AsyncMemoryBackend[int]):
    await backend.set_many([("foo", 42), ("bar", 100500)])
    assert backend.size == 2
    assert await backend.get_many("foo", "bar") == {"foo": 42, "bar": 100500}


@mark.asyncio
async def test_set_with_ttl(backend: AsyncMemoryBackend[int]):
    with freeze_time("2022-06-11 21:33:00"):
        await backend.set("foo", 42, timedelta(seconds=59))
    with freeze_time("2022-06-11 21:33:58"):
        assert await backend.get("foo") == 42
    with freeze_time("2022-06-11 21:34:00"):
        assert await backend.get("foo") is None
    assert backend.size == 0


@mark.asyncio
async def test_expire_at(backend: AsyncMemoryBackend[int]):
    await backend.set("foo", 42)
    await backend.expire_at("foo", datetime(2022, 6, 10, 21, 50, 00, tzinfo=timezone.utc))

    with freeze_time("2022-06-10 21:49:59"):
        assert await backend.get("foo") == 42
    with freeze_time("2022-06-10 21:50:00"):
        assert await backend.get("foo") is None
    assert backend.size == 0


@mark.asyncio
async def test_expire_in(backend: AsyncMemoryBackend[int]):
    with freeze_time("2022-06-10 21:49:00"):
        await backend.set("foo", 42)
        await backend.expire_in("foo", timedelta(seconds=59))
    with freeze_time("2022-06-10 21:50:00"):
        assert await backend.get("foo") is None
    assert backend.size == 0
