import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from espdata.models import SensorData
from datetime import datetime
from django.db.models import Avg, Max, Min

# Create your tests here.
date = datetime(2024, 12, 10).date()

report = SensorData.objects.filter(timestamp__date=date).aggregate(
    max_temp = Max('temperature'),
    min_temp = Min('temperature'),
    avg_temp = Avg('temperature'),
    max_hud = Max('humidity'),
    min_hud = Min('humidity'),
    avg_hud = Avg('humidity')
)

def send_email():
    sender_email = "lamtuanduc3003@gmail.com"
    password = "ratovcoemxtdjgjz"
    recipient_email = "mingbka@gmail.com"

    # Nội dung
    subject = f"""
    Báo cáo nhiệt độ độ ẩm ngày {date}
    """
    body = f"""
    Nhiệt độ:
    - Cao nhất: {report['max_temp']}
    """

    # Thiết lập email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Kết nối với SMTP server và gửi email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Bắt đầu kết nối an toàn
            server.login(sender_email, password)  # Đăng nhập
            server.sendmail(sender_email, recipient_email, msg.as_string())  # Gửi email
        print("Email đã được gửi thành công!")
    except Exception as e:
        print(f"Lỗi khi gửi email: {e}")