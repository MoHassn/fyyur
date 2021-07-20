import datetime, dateutil

# I came out with this approach after tens of searches on google and stackoverflow
# this answer helped me to compare the two differnt formates https://stackoverflow.com/a/41624199/11998654
def past(date_time):
  return dateutil.parser.parse(date_time).replace(tzinfo=datetime.timezone.utc) < datetime.datetime.now().replace(tzinfo=datetime.timezone.utc)
