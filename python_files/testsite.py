from datetime import datetime, timedelta

today = (datetime.today()+timedelta(hours=-4))
print today.time()