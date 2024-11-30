from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SensorData

# Create your views here.
@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            temperature = data.get('temperature')
            humidity = data.get('humidity')
            if temperature is not None and humidity is not None:
                SensorData.objects.create(temperature=temperature, humidity=humidity)
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Only POST allowed'}, status=405)

def display_data(request):
    data = SensorData.objects.all() #.order_by('-timestamp')[:10]  
    data_list = list(data)
    latest_item = data_list[-1] if data_list else None
    return render(request, 'espdata/display_data.html', {'latest_item': latest_item})