import datetime
import json


class DatetimeEncoder(json.JSONEncoder):
    def default(self, o):
        # if datetime object detected, return ISO8601 string
        if isinstance(o, datetime.datetime):
            return f"{o.isoformat('T')}Z"

        # otherwise pass it onto the default encoder
        return super().default(o)
