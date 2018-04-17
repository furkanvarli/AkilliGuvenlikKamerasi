import time
import RPi.GPIO as gpio
import io
import picamera
import cv2
import numpy
from email import encoders
import smtplib, time, getpass, datetime, socket
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

mail_gonderici = "furkanvarlive@gmail.com"
mail_sifresi = "15590271594f"
kime_gidecek = "furki3411@outlook.com"

baslik = "DIKKAT"
stream = io.BytesIO()

gpio.setmode(gpio.BCM)
pir_pin=18

while True:
    while True:
        gpio.setup(pir_pin, gpio.IN)
        if gpio.input(pir_pin):
            break
        else:
            time.sleep(1)

    time.sleep(0.5)

    with picamera.PiCamera() as camera:
        camera.resolution = (720, 520)
        camera.capture(stream, format='jpeg')

    buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

    image = cv2.imdecode(buff, 1)

    face_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.4.0/data/haarcascades/haarcascade_frontalface_alt.xml')

    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    print(str(len(faces))+" yuz tespit edildi")

    for (x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)

    cv2.imwrite('tespit.jpg',image)


    if len(faces) > 0:
        msg = MIMEMultipart()
        msg['From'] = mail_gonderici
        msg['To'] = kime_gidecek
        msg['Subject'] = baslik

        msg.attach(MIMEText("Kapinizda biri tespit edildi!", 'plain'))


        dosya_yolu = open("/home/pi/Desktop/tespit.jpg", "rb")
        dosya_adi = "tespit.jpg"

        part = MIMEBase('application', "octet-stream")
        part.set_payload((dosya_yolu).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename= %s' % dosya_adi)

        msg.attach(part)

        mesaj = msg.as_string()

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(mail_gonderici, mail_sifresi)
        server.sendmail(mail_gonderici, kime_gidecek, mesaj)
        print("E-mail başarıyla gönderildi")

    time.sleep(60)

    
   
    
