from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SystemStatus

def index(request):  # 간단 확인
   return render(request, 'monitor/index.html')

def dashboard(request):
    return render(request, 'monitor/dashboard.html')

@csrf_exempt
def report(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)
    data = json.loads(request.body.decode('utf-8'))
    SystemStatus.objects.create(
        hostname=data.get('hostname', 'unknown'),
        platform=data.get('platform', 'unknown'),
        cpu_percent=data.get('cpu_percent', 0),
        memory_percent=data.get('memory_percent', 0),
        disk_percent=data.get('disk_percent', 0),
        net_sent_MB=data.get('net_sent_MB', 0),
        net_recv_MB=data.get('net_recv_MB', 0),
        ping_ms=data.get('ping_ms'),
        download_Mbps=data.get('download_Mbps'),
        upload_Mbps=data.get('upload_Mbps'),
    )
    return JsonResponse({"status": "ok"})

def status_api(request):
    try:
        limit = int(request.GET.get('limit', '200'))
    except ValueError:
        limit = 200
    qs = SystemStatus.objects.order_by('-timestamp')[:limit]
    items = []
    for r in qs[::-1]:
        items.append({
            "timestamp": r.timestamp.isoformat(),
            "hostname": r.hostname,
            "platform": r.platform,
            "cpu": r.cpu_percent,
            "mem": r.memory_percent,
            "disk": r.disk_percent,
            "sent": r.net_sent_MB,
            "recv": r.net_recv_MB,
            "ping": r.ping_ms,
            "down": r.download_Mbps,
            "up": r.upload_Mbps,
        })
    return JsonResponse({"items": items})
