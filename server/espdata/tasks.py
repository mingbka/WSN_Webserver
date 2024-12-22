from celery import shared_task
from django.core.mail import send_mail
from django.db.models import Avg, Max, Min
from django.utils.timezone import now, timedelta
from .models import SensorData  # Thay bằng model lưu dữ liệu của bạn
from datetime import datetime

@shared_task
def send_daily_report_email():
    # Lấy dữ liệu trong 24 giờ qua
    date = datetime.now() - timedelta(hours=24)
    data = SensorData.objects.filter(timestamp__date=date)

    # Tính max, min, avg nhiệt độ và độ ẩm
    stats = data.aggregate(
        max_temperature=Max('temperature'),
        min_temperature=Min('temperature'),
        avg_temperature=Avg('temperature'),
        max_humidity=Max('humidity'),
        min_humidity=Min('humidity'),
        avg_humidity=Avg('humidity'),
    )

    # Tạo nội dung email
    subject = f"""
    Báo cáo ngày {date}
    """

    email_body = f"""
    Báo cáo nhiệt độ và độ ẩm trong 24 giờ qua:

    Nhiệt độ:
    - Cao nhất: {stats['max_temperature']}°C
    - Thấp nhất: {stats['min_temperature']}°C
    - Trung bình: {stats['avg_temperature']:.1f}°C

    Độ ẩm:
    - Cao nhất: {stats['max_humidity']}%
    - Thấp nhất: {stats['min_humidity']}%
    - Trung bình: {stats['avg_humidity']:.1f}%
    """

    # Lấy danh sách email người dùng
    from django.contrib.auth.models import User
    users = User.objects.all()
    users={"Minh":{
        "email":"mingbka@gmail.com"
    }}

    # Gửi email
    for user in users:
        send_mail(
            subject=subject,
            message=email_body,
            from_email='lamtuanduc3003@gmail.com',
            recipient_list=[user.email],
        )

    return f'Sent email to {users.count()} users'
