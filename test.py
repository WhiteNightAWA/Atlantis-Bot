import datetime

print(
    datetime.datetime.utcnow().replace(microsecond=0).timestamp(),

    datetime.datetime.now().replace(microsecond=0).timestamp()
)
