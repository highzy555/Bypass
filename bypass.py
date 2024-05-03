from fbchat import Client, ThreadType
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import os
from flask import Flask, render_template
from threading import Thread
app = Flask('')
@app.route('/')
def home():
  return "bot python is online!"
def index():
  return render_template("index.html")
def run():
  app.run(host='0.0.0.0', port=8080)
def high():
  t = Thread(target=run)
  t.start()

# เบอร์โทรศัพท์สำหรับใส่ในซองอั่งเปาทรูมันนี่วอเล็ต
phone_number = os.environ['number']
email = os.environ['mail']
password = os.environ['pass']
high()

# ฟังก์ชันสำหรับการตรวจสอบลิงก์ซองอั่งเปาทรูมันนี่วอเล็ต
def is_truemoney_angpao_link(link):
    pattern = r'https?://www\.facebook\.com/\w+/posts/\w+'
    return bool(re.match(pattern, link))

# ฟังก์ชันสำหรับการรับซองอั่งเปาทรูมันนี่วอเล็ตและใส่เบอร์
def receive_truemoney_angpao(link):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # ทำงานในโหมดไร้หน้าต่าง
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(link)

        # หาปุ่มรับซองอั่งเปาและคลิก
        receive_button = driver.find_element_by_xpath("//button[contains(text(), 'รับซองอั่งเปา')]")
        receive_button.click()

        # หาช่องกรอกเบอร์โทรศัพท์และกรอก
        phone_input = driver.find_element_by_xpath("//input[@placeholder='เบอร์โทรศัพท์มือถือ']")
        phone_input.send_keys(phone_number)

        # หาปุ่มยืนยันและคลิก
        confirm_button = driver.find_element_by_xpath("//button[contains(text(), 'ยืนยัน')]")
        confirm_button.click()

        driver.quit()
        return True
    except Exception as e:
        print(f'Error receiving TrueMoney angpao: {e}')
        return False

# ฟังก์ชันสำหรับการจัดการข้อความ
def handle_message(message_object, client, author_id):
    message = message_object.text

    if any(is_truemoney_angpao_link(word) for word in message.split()):
        links = [word for word in message.split() if is_truemoney_angpao_link(word)]
        for link in links:
            success = receive_truemoney_angpao(link)
            if success:
                client.send(ThreadType.USER, author_id, f'ขอบคุณสำหรับซองอั่งเปาทรูมันนี่วอเล็ต! เบอร์ {phone_number} ได้รับซองแล้ว')
            else:
                client.send(ThreadType.USER, author_id, 'เกิดข้อผิดพลาดในการรับซองอั่งเปาทรูมันนี่วอเล็ต')

# เริ่มบอท
client = Client(email, password)
client.listen(handle_message)
