from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SensorData
from django.utils.timezone import localtime
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
from django.db.models import Avg, Max, Min
from datetime import datetime, timedelta
import pandas as pd
import os

# Create your views here.
@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            node = data.get('node')
            temperature = data.get('temperature')
            humidity = data.get('humidity')

            if temperature is not None and humidity is not None and node is not None :
                SensorData.objects.create(node=node, temperature=temperature, humidity=humidity)
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Only POST allowed'}, status=405)

def display_data(request):
    node_1_data = SensorData.objects.filter(node=1).last()  # Lấy dữ liệu mới nhất của node 1
    node_1_data.timestamp = localtime(node_1_data.timestamp)
    node_2_data = SensorData.objects.filter(node=2).last()  # Lấy dữ liệu mới nhất của node 2
    node_2_data.timestamp = localtime(node_2_data.timestamp)
    node_3_data = SensorData.objects.filter(node=3).last()  # Lấy dữ liệu mới nhất của node 3
    node_3_data.timestamp = localtime(node_3_data.timestamp)

    # dữ liệu để vẽ biểu đồ
    now = datetime.now()
    start_date = now - timedelta(days=1)
    # date = datetime(2024,12,18).date()  # kiểm thử

    sensor_data_dict={}
    chart_data_dict={}

    for i in range(1,4):
        sensor_data_dict[f"sensor_data_{i}"] = SensorData.objects.filter(
        timestamp__range=(start_date, now), 
        node=i
        ).order_by('timestamp') # sắp xếp dữ liệu theo thứ tự thời gian

        chart_data_dict[f"chart_data_node_{i}"]=[]

        for data in sensor_data_dict[f"sensor_data_{i}"]:
            local_timestamp = localtime(data.timestamp).timestamp()
            chart_data_dict[f"chart_data_node_{i}"].append({
                'time': int(local_timestamp),
                'temperature': data.temperature,
                'humidity': data.humidity,
            })
    chart_data_node_1 = chart_data_dict["chart_data_node_1"]
    chart_data_node_2 = chart_data_dict["chart_data_node_2"]
    chart_data_node_3 = chart_data_dict["chart_data_node_3"]
    
    return render(request, 'espdata/display_data.html', {
        'node_1_data': node_1_data,
        'node_2_data': node_2_data,
        'node_3_data': node_3_data,
        'chart_data_node_1': chart_data_node_1,
        'chart_data_node_2': chart_data_node_2,
        'chart_data_node_3': chart_data_node_3,
    })
    
def daily_report(request):
    end = datetime.now()
    start = end - timedelta(days=1)

    data = SensorData.objects.filter(timestamp__range=(start, end)).values()

    if not data.exists():
        return JsonResponse({"message": "Không có dữ liệu trong vòng 1 ngày qua."}, status=404)

    report=[]

    for i, record in enumerate(data, start=1):
        record.pop('id', None)
        time = record['timestamp'] + timedelta(hours=7)
        h_m = time.strftime(' %H:%M ') 
        new_record = {'ordinal': i, **record, 'timestamp': h_m}
        report.append(new_record)

    df = pd.DataFrame(report)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="data_last_day.xlsx"'

    # Ghi file Excel vào response
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sensor Data')

    return response
    

    
