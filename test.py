import datetime
import requests


t = datetime.datetime.utcnow()


data = requests.put("https://datetimecord.rauf.wtf/", data=t)

print(data)
print(data.json())
