import pytest
from voice_commands.apps.clock.alarm.provider.alarm_provider import ProviderAlarm
from stark.core.types import String
from voice_commands.parameters import Time
from voice_commands.apps.clock.alarm.parameters.time_alarm import WeekDay
import schedule



@pytest.fixture()
def provider():
    return ProviderAlarm()


@pytest.mark.parametrize(
    "name, expected_substr",
    [
        ("Подъем", "Подъем"),
        ("Будильник", "Будильник"),
        ("Пробуждение", "Пробуждение"),
    ]
)
def test_add_name(provider, name, expected_substr):
    name = String(name)
    provider.add_name(name)
    assert provider.name == expected_substr


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "days, expected_days",
    [
        ("шесть тридцать", "06:30"),
        ("двенадцать ноль ноль", "12:00"),  
        ("восемь пятнадцать", "08:15"),
    ]
)
async def test_add_time(provider, days, expected_days):
    time = Time(None)
    await time.did_parse(days)
    provider.add_target_time(time)
    assert provider.target_time == expected_days



@pytest.mark.asyncio
@pytest.mark.parametrize(
    "day, expected_days",
    [
        ("понедельник вторник", [("понедельник", schedule.every().monday), ("вторник", schedule.every().tuesday)]),
        ("среда четверг", [("среда", schedule.every().wednesday), ("четверг", schedule.every().thursday)]),
    ]
)
async def test_add_day(provider, day, expected_days):
    week_day = WeekDay(None)
    await week_day.did_parse(day)
    provider.add_day(week_day)
    assert [d[0] for d in provider.day] == [d[0] for d in expected_days]

    assert all(isinstance(d[1], schedule.Job) for d in provider.day)


@pytest.mark.parametrize(
    "name, target_time, day_name, day_job",
    [
        ("Будильник", "08:00", "понедельник", schedule.every().monday),
        ("Работа", "09:30", "вторник", schedule.every().tuesday),
    ]
)
def test_start_alarm(provider, name, target_time, day_name, day_job):
    provider.name = name
    provider.target_time = target_time
    provider.day = [(day_name, day_job)]

    provider.start_alarm()

    jobs = provider.model.list_jobs[name]
    assert jobs[0][0] == target_time
    assert jobs[0][1] == day_name

    job = jobs[0][2]
    assert isinstance(job, schedule.Job)
    assert job.at_time.strftime("%H:%M") == target_time


@pytest.mark.parametrize(
    "name, target_time, days",
    [
        (
            "Будильник",
            "08:00",
            [("понедельник", schedule.every().monday), ("вторник", schedule.every().tuesday)],
        ),
        (
            "Работа",
            "09:30",
            [("среда", schedule.every().wednesday), ("четверг", schedule.every().thursday)],
        ),
    ]
)
def test_start_alarm_multiple_days(provider, name, target_time, days):
    provider.name = name
    provider.target_time = target_time
    provider.day = days

    provider.start_alarm()

    jobs = provider.model.list_jobs[name]


    assert len(jobs) == len(days)

    for idx, (expected_day_name, _) in enumerate(days):
        saved_time, saved_day, job = jobs[idx]

        assert saved_time == target_time
        assert saved_day == expected_day_name

        assert isinstance(job, schedule.Job)
        assert job.at_time.strftime("%H:%M") == target_time