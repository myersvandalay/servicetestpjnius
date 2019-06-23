'p4a example service using oscpy to communicate with main application.'
from random import sample, randint
from string import ascii_letters
from time import localtime, asctime, sleep
from plyer import notification
from plyer.utils import platform
from plyer.compat import PY2
from time import sleep
from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient

CLIENT = OSCClient('localhost', 3002)

def do_notify(title, message, ticker):
    if PY2:
        title = title.decode('utf8')
        message = message.decode('utf8')
    kwargs = {'title': title, 'message': message, 'ticker': ticker}
    """
    if mode == 'fancy':
        kwargs['app_name'] = "Plyer Notification Example"
        if platform == "win":
            kwargs['app_icon'] = join(dirname(realpath(__file__)),
                                      'plyer-icon.ico')
            kwargs['timeout'] = 4
        else:
            kwargs['app_icon'] = join(dirname(realpath(__file__)),
                                      'plyer-icon.png')
    elif mode == 'toast':
        kwargs['toast'] = True
    """
    kwargs['app_name'] = "A kivy test"
    notification.notify(**kwargs)




def ping(*_):
    'answer to ping messages'
    CLIENT.send_message(
        b'/message',
        [
            ''.join(sample(ascii_letters, randint(10, 20)))
            .encode('utf8'),
        ],
    )
    do_notify("testing Title", "testmess", "testtick")
    sleep(14)
    do_notify("delay title", "testdelay", "testtickdelay")



def send_date():
    'send date to the application'
    CLIENT.send_message(
        b'/date',
        [asctime(localtime()).encode('utf8'), ],
    )


if __name__ == '__main__':
    SERVER = OSCThreadServer()
    SERVER.listen('localhost', port=3000, default=True)
    SERVER.bind(b'/ping', ping)
    while True:
        sleep(1)
        send_date()
