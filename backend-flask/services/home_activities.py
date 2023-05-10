from datetime import datetime, timedelta, timezone
from opentelemetry import trace

from lib.db import db

tracer = trace.get_tracer("home.activities")
class HomeActivities:
  def run(cognito_user_id=None):
    ##logger.info("HomeActivities")
    #with tracer.start_as_current_span("home-activities-data") as outer_span:
    #  outer_span.set_attribute("outer", True)
    #  span = trace.get_current_span()
    #  now = datetime.now(timezone.utc).astimezone()
    #  span.set_attribute("app.hubabuba", now.isoformat())
      sql = db.template('activities','home')
      results = db.query_array_json(sql)
    #  with tracer.start_as_current_span("home-results-activities") as inner_span:
    #    inner_span.set_attribute("inner", True)
    #    span = trace.get_current_span()
    #    span.set_attribute("app.result_length", len(sql))
      return results