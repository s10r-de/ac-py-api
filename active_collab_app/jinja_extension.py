from jinja2 import pass_eval_context as eval_context
from jinja2.ext import Extension

from active_collab_app.helper import format_timestamp_as_date, format_timestamp_as_datetime


@eval_context
def as_date(_eval_ctx, ts: int) -> str:
    return format_timestamp_as_date(ts)

@eval_context
def as_datetime(_eval_ctx, ts: int) -> str:
    return format_timestamp_as_datetime(ts)

@eval_context
def email(_eval_ctx, addr: str) -> str:
    return f'<a class="email" href="mailto:{addr}">&lt;{addr}&gt;</a>'

class JinjaFilters(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.filters["as_date"] = as_date
        environment.filters["as_datetime"] = as_datetime
        environment.filters["email"] = email

    def parse(self, _parser):
        pass
