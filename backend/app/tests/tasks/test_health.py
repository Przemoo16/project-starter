from app.tasks import health


def test_check_health() -> None:
    task = health.check_health.apply()

    assert task.status == "SUCCESS"
