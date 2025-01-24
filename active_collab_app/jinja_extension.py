import json

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

@eval_context
def to_json(_eval_ctx, data: dict) -> str:
    return "<textarea>{}</textarea>".format(json.dumps(data, indent=2))

reactions = {
    "ThumbsUpReaction": "👍",
    "ApplauseReaction": "👏",
    "SmileReaction": "😀",
    "HeartReaction": "♥️",
    "PartyReaction": "🎉",
    "ThinkingReaction": "🤔",
    "ThumbsDownReaction": "👎",
}

@eval_context
def to_emoji(_eval_ctx, reaction) -> str:
    fallback_emoji = "�"
    return reactions.get(reaction) or fallback_emoji

class JinjaFilters(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.filters["as_date"] = as_date
        environment.filters["as_datetime"] = as_datetime
        environment.filters["email"] = email
        environment.filters["json"] = to_json
        environment.filters["emoji"] = to_emoji

    def parse(self, _parser):
        pass
