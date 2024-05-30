from django.db.models import aggregates
from django.db.models import expressions
from django.db.models import fields
from django.db.models import functions

from exam.models import ExamDAO
from . import models


DATE_START_HOUR = 6


def get_calendar(user: models.UserDAO) -> None:
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
    queryset = queryset.values('date')
    queryset = queryset.annotate(
        count=aggregates.Count('date'),
    )
    queryset = queryset.order_by('-date')
    return {
        'calendar': {
            str(date): count for date, count in queryset.values_list('date', 'count')
        }
    }
