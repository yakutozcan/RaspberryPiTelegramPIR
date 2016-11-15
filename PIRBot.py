from gpiozero import MotionSensor
import telepot
import time
from datetime import timedelta


pir = MotionSensor(4)
chat_listen = {}
# chat_listen_switch = False

def handle(msg):
#    global chat_listen_switch
    chat_id = msg['chat']['id']
    command = msg['text']

    print 'Got command: %s' % command

    if command == '/StartListenMotion':
#        chat_listen_switch = True
        if chat_id not in chat_listen:
            chat_listen[chat_id] = True
            bot.sendMessage(chat_id, "Started Listen Motion")
        elif chat_listen[chat_id]:
            bot.sendMessage(chat_id, "Already Listening")
        else:
            chat_listen[chat_id] = True
            bot.sendMessage(chat_id, "Restarted Listen Motion")
        print "%s said it want to be notified" % chat_id

    elif command == '/StopListenMotion':
#        chat_listen_switch = False
        if chat_id not in chat_listen:
            chat_listen[chat_id] = False
            bot.sendMessage(chat_id, "Wasn't Listening Motion")
        elif chat_listen[chat_id]:
            chat_listen[chat_id] = False
            bot.sendMessage(chat_id, "Stopped Listening")
        else:
            bot.sendMessage(chat_id, "Wasn't Listen Motion")
        print "%s said it doesn't want to be notified" % chat_id

    elif command == '/uptime':
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            uptime_string = str(timedelta(seconds=uptime_seconds))
            bot.sendMessage(chat_id, uptime_string)
            print "%s said it want the uptime" % chat_id


def notify_motion():
    notify("Motion Detected")


def notify_no_motion():
    notify("Motion Stopped")


def notify(msg):
    for chat_id, listening in chat_listen.items():
#        if chat_listen_switch:
        if listening:
            bot.sendMessage(chat_id, msg)

pir.when_motion = notify_motion
pir.when_no_motion = notify_no_motion

bot = telepot.Bot('292346928:AAFkTCWYOBW7Xq19Utg8pCgs2fBXIRfKdcg')
bot.message_loop(handle)
print 'I am listening ...'

while True:
    time.sleep(10)
