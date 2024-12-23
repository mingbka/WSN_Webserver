from django.test import TestCase
from espdata.models import SensorData
from datetime import datetime
import pandas as pd
import os

# Create your tests here.
date = datetime(2024, 12, 10).date()

report = SensorData.objects.filter(timestamp__date=date).values()

for record in report:
    for key, value in record.items():
        if isinstance(value, pd.Timestamp):  # Kiểm tra xem giá trị có phải là datetime không
            # Loại bỏ múi giờ nếu có
            record[key] = value.replace(tzinfo=None)

df = pd.DataFrame(report)

output_dir = os.path.join(os.getcwd(), 'exports')
os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(output_dir, f"data_{date}.xlsx")
df.to_excel(output_file, index=False)

print(f"File Excel đã được lưu tại: {output_file}")