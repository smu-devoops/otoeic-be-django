import datetime
import typing

from django.db.models import aggregates
from django.db.models import expressions
from django.db.models import fields
from django.db.models import functions
from django.db.models import QuerySet
from rest_framework import exceptions

from exam.models import ExamDAO
from . import models


DATE_START_HOUR = 6
PRICE_STREAK_FREEZE = 640


def get_calendar(user: models.UserDAO) -> typing.Dict[datetime.date, int]:
    queryset = _get_calendar_queryset(user)
    return {
        'calendar': {
            str(date): count for date, count in queryset.values_list('date', 'count')
        }
    }


def update_streak(user: models.UserDAO) -> None:
    """사용자의 streak를 업데이트한다.

    streak는 연속으로 문제를 푼 날의 수를 의미한다.
    """
    date_today = datetime.date.today()

    if user.date_streak_should_be_updated < date_today:
        calendar = _get_calendar_queryset(user) # 빠르게 조회하기 위해 미리 쿼리셋을 가져온다.

        while user.date_streak_should_be_updated < date_today:
            # 오늘 이전까지 streak가 업데이트 되지 않은 날이 있으면 streak를 업데이트한다.

            if calendar.filter(date=user.date_streak_should_be_updated).exists():
                # 해당 날짜에 시험을 제출했으면 streak를 1 증가시킨다.
                user.streak += 1

            elif _should_use_streak_freeze(user):
                # 시험을 제출하지 않았어도 streak freeze가 활성화 되어 있으면 streak를 유지한다.
                user.freeze_amount -= 1

            else:
                # 시험을 제출하지 않아 streak이 끊겼다.
                user.streak = 0

            user.date_streak_should_be_updated += datetime.timedelta(days=1)

    if _did_submit_exam(user, date_today):
        # 오늘 시험을 제출했으면 streak를 1 증가시킨다.
        user.streak += 1
        user.date_streak_should_be_updated = date_today + datetime.timedelta(days=1)

    user.save()


def _did_submit_exam(user: models.UserDAO, date: datetime.date) -> bool:
    """사용자가 date에 시험을 제출했는지 여부를 반환한다."""
    queryset = ExamDAO.objects
    queryset = queryset.filter(user_created=user)
    queryset = queryset.filter(
        date_submitted__date=date,
    )
    return queryset.exists()


def _should_use_streak_freeze(user: models.UserDAO) -> bool:
    """streak freeze를 사용할 수 있는지 여부를 반환한다."""
    return bool(
        user.streak > 0 and
        user.freeze_activated and
        user.freeze_amount > 0
    )


def _get_calendar_queryset(user: models.UserDAO) -> QuerySet:
    """Get calendar queryset for user.

    Returns: `QuerySet[date: date, count: int]`
    """
    queryset = ExamDAO.objects
    queryset = queryset.filter(user_created=user)
    queryset = queryset.exclude(date_submitted=None)
    queryset = queryset.annotate(
        date=functions.TruncDate(
            expressions.ExpressionWrapper(
                expressions.Func(
                    expressions.F('date_submitted'),
                    function='DATETIME',
                    template='%(function)s(%(expressions)s, %(interval)s)',
                    interval=f"'-{DATE_START_HOUR} hours'",
                ),
                output_field=fields.DateTimeField(),
            )
        ),
    )
    # date 기준으로 GROUP BY 한 후, COUNT 한다.
    queryset = queryset.values('date')
    queryset = queryset.annotate(
        count=aggregates.Count('date'),
    )
    return queryset.order_by('-date')


def buy_streak_freeze(user: models.UserDAO) -> None:
    """streak freeze를 구매한다."""
    if user.point < PRICE_STREAK_FREEZE:
        raise exceptions.ValidationError(detail=(
            f"Not enough point to buy streak freeze."
        ))
    user.point -= PRICE_STREAK_FREEZE
    user.freeze_amount += 1
    user.save()
