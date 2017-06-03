from gpiozero import MotionSensor
import telepot
import picamera
import time
from datetime import timedelta


pir = MotionSensor(4)
chat_listen = {}
# chat_listen_switch = False

def handle(msg):
#    global chat_listen_switch
    chat_id = msg['chat']['id']
    command = msg['text']

    print 'Gelen Komut: %s' % command

    if command == '/HareketDinlemeyeBasla':
#        chat_listen_switch = True
        if chat_id not in chat_listen:
            chat_listen[chat_id] = True
            bot.sendMessage(chat_id, "Dinlemeye Basladi")
        elif chat_listen[chat_id]:
            bot.sendMessage(chat_id, "Zaten Dinleniyor")
        else:
            chat_listen[chat_id] = True
            bot.sendMessage(chat_id, "Dinleme Yeniden Basladi")

    elif command == '/HareketDinlemeyiDurdur':
#        chat_listen_switch = False
        if chat_id not in chat_listen:
            chat_listen[chat_id] = False
            bot.sendMessage(chat_id, "Dinleme Etkin Değildi")
        elif chat_listen[chat_id]:
            chat_listen[chat_id] = False
            bot.sendMessage(chat_id, "Dinleme Durduruldu")
        else:
            bot.sendMessage(chat_id, "Dinleme Etkin Değil")

    elif command == '/NeZamandirCalisiyorsun':
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            uptime_string = str(timedelta(seconds=uptime_seconds))
            bot.sendMessage(chat_id, uptime_string)

    elif command == '/ResimCek':
            camera = picamera.PiCamera()
            camera.capture('capture.jpg')
            camera.close()
            bot.sendPhoto(chat_id, photo=open('capture.jpg', 'rb'))
    else:
            bot.sendMessage(chat_id, 'Komut Bulunamadi')
            bot.sendMessage(chat_id, 'Kayitli Komutlar \n'
                                     '/NeZamandirCalisiyorsun \n'
                                     '/HareketDinlemeyiDurdur \n'
                                     '/HareketDinlemeyeBasla \n'
                                     '/ResimCek')


def notify_motion():
    notify("Hareket Algilandi")


def notify_no_motion():
    notify("Hareketli Durdu")


def notify(msg):
    for chat_id, listening in chat_listen.items():
#        if chat_listen_switch:
        if listening:
            bot.sendMessage(chat_id, msg)
            #Get the photo
            camera = picamera.PiCamera()
            camera.capture('capture.jpg')
            camera.close()
            bot.sendPhoto(chat_id, photo=open('capture.jpg', 'rb'))

pir.when_motion = notify_motion
pir.when_no_motion = notify_no_motion

bot = telepot.Bot('292346928:AAFkTCWYOBW7Xq19Utg8pCgs2fBXIRfKdcg')
bot.message_loop(handle)
print 'Uygulama Calisti'

while True:
    time.sleep(10)
