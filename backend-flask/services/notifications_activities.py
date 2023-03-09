from datetime import datetime, timedelta, timezone
from aws_xray_sdk.core import xray_recorder
class NotificationsActivities:
  def run():
    # Start a segment
    segment = xray_recorder.begin_segment('backend_notifications')
    now = datetime.now(timezone.utc).astimezone()
    xray_dict = {'now': now.isoformat()}
    segment.put_metadata('key', xray_dict, 'namespace')
    subsegment = xray_recorder.begin_subsegment('sub_xray_backend')
    subsegment.put_annotation('end_notifications', now.isoformat())
    results = [{
      'uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
      'handle':  'Donal Duck',
      'message': 'Cloud is Future!',
      'created_at': (now - timedelta(days=2)).isoformat(),
      'expires_at': (now + timedelta(days=5)).isoformat(),
      'likes_count': 5,
      'replies_count': 1,
      'reposts_count': 0,
      'replies': [{
        'uuid': '26e12864-1c26-5c3a-9658-97a10f8fea67',
        'reply_to_activity_uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
        'handle':  'Worf',
        'message': 'This post has no honor!',
        'likes_count': 0,
        'replies_count': 0,
        'reposts_count': 0,
        'created_at': (now - timedelta(days=2)).isoformat()
        }],
      }
    ]
    return results
    xray_recorder.end_subsegment()
    xray_recorder.end_segment()