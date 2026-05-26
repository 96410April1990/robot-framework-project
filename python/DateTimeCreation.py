from datetime import datetime, timedelta

current_date_time = datetime.now()

formatted_date_time = current_date_time.strftime("%Y-%m-%d %H:%M:%S")
print("Current Date and Time:", formatted_date_time)

future_date = current_date_time + timedelta(days=5)
formatted_future_date = future_date.strftime("%Y-%m-%d %H:%M:%S")
print("Date and Time after 5 days:", formatted_future_date)
