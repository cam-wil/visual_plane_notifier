from time import sleep, time
import json
import socket
import threading
import board
import neopixel

pixel_pin = board.D18

ORDER = neopixel.GRB

num_pixels = 9

GREEN = (0,100,0)
RED = (100,0,0)
BLUE = (0,0,0)

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 30154  # The port used by the server

working_dst = 999.9

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

def set_color(p,r,g,b): #position, red, green, blue
   print("set_color")
   pixels[p] = (r,g,b)
   pixels.show()

def set_all(r,g,b): #position, red, green, blue
   print("set_all")
   for i in range(num_pixels):
       pixels[i] = (r,g,b)
   pixels.show()

def clear_all():
    print("clear_all")
    for i in range(num_pixels):
        pixels[i] = (0,0,0)
    pixels.show()

def mode_calc(dist):
    global working_dst
    print("mode_calc: " + str(dist))
    if working_dst >= 0 and working_dst < 5:
        set_mode(8)
    elif working_dst >= 5 and working_dst < 10:
        set_mode(7)
    elif working_dst >= 10 and working_dst < 15:
        set_mode(6)
    elif working_dst >= 15 and working_dst < 20:
        set_mode(5)
    elif working_dst >= 20 and working_dst < 25:
        set_mode(4)
    elif working_dst >= 25 and working_dst < 30:
        set_mode(3)
    elif working_dst >= 30 and working_dst < 40:
        set_mode(2)
    elif working_dst >= 40 and working_dst < 60:
        set_mode(1)
    elif working_dst >= 60 and working_dst < 300:
        set_mode(0)
        
def set_mode(mode): #mode 0 - 8. Increasing mode with closer plane
    print("set mode: " + str(mode))
    if mode == 0:
        clear_all()
        set_color(0,0,125,0)
    elif mode == 1:
        clear_all()
        set_color(0,0,125,0)
        set_color(1,0,125,0)
    elif mode == 2:
        set_color(0,0,125,0)
        set_color(1,0,125,0)
        set_color(2,0,125,0)
    elif mode == 3:
        set_color(0,0,125,0)
        set_color(1,0,125,0)
        set_color(2,0,125,0)
        set_color(3,0,125,0)
    elif mode == 4:
        set_color(0,0,125,0)
        set_color(1,0,125,0)
        set_color(2,0,125,0)
        set_color(3,0,125,0)
        set_color(4,0,125,0)
    elif mode == 5:
        set_color(0,0,125,0)
        set_color(1,0,125,0)
        set_color(2,0,125,0)
        set_color(3,0,125,0)
        set_color(4,0,125,0)
        set_color(5,0,125,0)
    elif mode == 6:
        set_color(0,0,125,0)
        set_color(1,0,125,0)
        set_color(2,0,125,0)
        set_color(3,0,125,0)
        set_color(4,0,125,0)
        set_color(5,0,125,0)
        set_color(6,0,125,0)
    elif mode == 7:
        set_color(0,0,125,0)
        set_color(1,0,125,0)
        set_color(2,0,125,0)
        set_color(3,0,125,0)
        set_color(4,0,125,0)
        set_color(5,0,125,0)
        set_color(6,0,125,0)
        set_color(7,0,125,0)
    elif mode == 8:
        set_color(0,125,0,0)
        set_color(1,125,0,0)
        set_color(2,125,0,0)
        set_color(3,125,0,0)
        set_color(4,125,0,0)
        set_color(5,125,0,0)
        set_color(6,125,0,0)
        set_color(7,125,0,0)
        set_color(8,125,0,0)
        

def start_socket():
    global working_dst
    trigger_cleared = False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        trig_time = time() - (60*4)
        sleep(4)

        while True:
            data = s.recv(1024 * 10)
            try:
                dat = json.loads(data)
                #print(str(dat["hex"]) + " " + str(dat["r_dst"]))
                #if (dat["hex"][:2] == "ae"): #if us military aircraft
                if(dat["hex"] == str("add66c")):
                    print("passed check")
                    trig_time = time() + (60*3) #time plus 3 minutes
                    working_dst = float(dat["r_dst"])
                    print("r_dst: " + str(dat["r_dst"]))
                    mode_calc(working_dst)
                    trigger_cleared = False
            except Exception as e:
                print(e)
            if time() > trig_time and not trigger_cleared:
               print("clear all in time trigger")
               clear_all()
               trigger_cleared = not trigger_cleared


# startup sequence
startup_toggle = False
for i in range(10):
    clear_all()
    if startup_toggle:
        set_all(200,0,0)
    else:
        set_all(0,200,0)
    sleep(0.5)
    startup_toggle = not startup_toggle

clear_all()

threading.Thread(target=start_socket).start()