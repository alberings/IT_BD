from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Event
import logging
import json
from django.core.serializers import serialize
from datetime import datetime, timedelta
from django.db.models import Count, Q

logger = logging.getLogger(__name__)

class EventAPIView(APIView):
    def post(self, request, *args, **kwargs):
        event_data = request.data
        event = Event.objects.create(
            type=event_data.get('type'),
            path=event_data.get('path'),
            details=event_data,
            # user_id=event_data.get('userId')
        )
        logger.info(f"Event received: {event}")
        return Response({"status": "success"}, status=201)


# def event_statistics(request):
#     # Retrieve all event records from the database
#     events = Event.objects.all()
#     # You can perform aggregation or data processing here if needed
   
#     return render(request, 'statistics.html', {'events': events})

# 
def parse_datetime(dt_str):
    return datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S.%fZ')

def event_statistics(request):
    path = request.GET.get('path', None)
    events = Event.objects.filter(path__icontains=path).order_by('timestamp') if path else Event.objects.all().order_by('timestamp')

    events_json = serialize('json', events)
    events_data = [event['fields'] for event in json.loads(events_json)]

    scroll_sessions = {}
    last_event_time = None
    session_id = 0
    last_event_type = None
    for event in events_data:
        event_time = parse_datetime(event['timestamp'])
        if event['type'] == 'scroll':
            if last_event_time and (event_time - last_event_time > timedelta(minutes=1) or last_event_type != 'scroll'):
                session_id += 1
            session_key = (event['path'], session_id)
            if session_key not in scroll_sessions:
                scroll_sessions[session_key] = event
            else:
                max_depth = max(float(scroll_sessions[session_key]['details']['depth']), float(event['details']['depth']))
                scroll_sessions[session_key]['details']['depth'] = "{:.2f}".format(max_depth)
        last_event_time = event_time
        last_event_type = event['type']

    success_paths = [
        'http://127.0.0.1:3000/payment/stripe/',
        'http://127.0.0.1:3000/payment/paypal/'
    ]
    payment_pageviews = Event.objects.filter(path__in=success_paths).count()
    total_pageviews = Event.objects.filter(type='pageview').count()

    payment_percentage = (payment_pageviews / total_pageviews * 100) if total_pageviews > 0 else 0

    success_events = Event.objects.filter(path__in=success_paths).order_by('timestamp')
    success_json = serialize('json', success_events)
    success_data = [event['fields'] for event in json.loads(success_json)]

    success_list = [{
        'path': event['path'],
        'timestamp': event['timestamp']
    } for event in success_data]

    final_events = list(scroll_sessions.values()) + [event for event in events_data if event['type'] != 'scroll']

    if path:
        pageview_counts = Event.objects.filter(path__icontains=path, type='pageview').values('path').annotate(count=Count('id'))
    else:
        pageview_counts = Event.objects.filter(type='pageview').values('path').annotate(count=Count('id'))
    pageview_counts_data = {item['path']: item['count'] for item in pageview_counts}
    pageview_counts_json = json.dumps(pageview_counts_data)

    context = {
        'successes': success_list,
        'events': final_events,
        'events_json': json.dumps(final_events),
        'pageview_counts_json': pageview_counts_json,
        'payment_percentage': payment_percentage
    }
    return render(request, 'statistics.html', context)

# def event_statistics(request):
#     events = Event.objects.all()
#     # Serialize the queryset to JSON string
#     events_json = serialize('json', events)
#     # Send events as a JSON response to be used by JavaScript
#     return render(request, 'statistics.html', {'events': events_json})

def payment_success(request):
    # Define the full success paths according to your database entries
    success_paths = [
        'http://127.0.0.1:3000/payment/stripe/',
        'http://127.0.0.1:3000/payment/paypal/'
    ]
    
    # Filter events for success paths
    success_events = Event.objects.filter(path__in=success_paths).order_by('timestamp')
    
    # Serialize to JSON for processing
    events_json = serialize('json', success_events)
    events_data = [event['fields'] for event in json.loads(events_json)]
    
    # Prepare data for display
    success_data = [{
        'path': event['path'],
        'timestamp': event['timestamp']
    } for event in events_data]

    return render(request, 'payment_success.html', {'successes': success_data})