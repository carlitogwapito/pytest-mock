import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize("outcome", ["return", "raise"])
async def test_async_spy_reset_clears_outcomes_and_await_history(mocker, outcome):
    class Subject:
        async def call(self, fail):
            if fail:
                raise ValueError("async failure")
            return 42

    subject = Subject()
    spy = mocker.spy(subject, "call")
    if outcome == "return":
        assert await subject.call(False) == 42
        assert spy.spy_return == 42
    else:
        with pytest.raises(ValueError, match="async failure"):
            await subject.call(True)
        assert isinstance(spy.spy_exception, ValueError)

    assert spy.call_count == 1
    assert spy.await_count == 1
    mocker.resetall()
    assert spy.call_count == 0
    assert spy.await_count == 0
    assert spy.spy_return is None
    assert spy.spy_exception is None
    assert spy.spy_return_list == []
    assert spy.spy_return_iter is None

    assert await subject.call(False) == 42
    assert spy.call_count == 1
    assert spy.await_count == 1
    assert spy.spy_return == 42
    assert spy.spy_exception is None
