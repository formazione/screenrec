import os
import glob
import tkinter as tk
# from sounddevice import query_devices


x = 0

def ask():
    file_root = "G:\\video\\"
    filename = input("Nome del file: ")
    filepath = file_root + filename + ".mp4"
    return filepath, file_root

def automatic_name():
    "Crea il nome da solo / ora chiedo il nome del file prima"
    global x

    fld = "G:\\video"
    if not fld + str(x) + ".mp4" in glob.glob(fld + "*.mp4"):
        filename = fld + str(x) + ".mp4"
    else:
        x += 1
        record()
    filename = fld + filename + ".mp4"
    return filename


def get_mic_name():
    "Uses sounddevice to get the name of the mic in case it changed"
    s = query_devices()
    audio = f"""{s[1]["name"]})"""
    return audio


def radiobutton(root, rbvar, text):
    global radio_cnt

    radio_cnt +=1
    rb = tk.Radiobutton(
        root,
        text=text,
        variable=rbvar,
        value=radio_cnt)
    rb.pack()
    return rb


def label(root, text):
    ck1 = tk.Label(root, text=text)
    ck1.pack()
    return ck1


def print_me():
    print("Destroyed")

radio_cnt = 0
def window():

    root = tk.Tk()
    lab = label(root, "Microfono")
    mic = tk.IntVar()
    ck1 = radiobutton(root, mic, "Cuffia")
    ck2 = radiobutton(root, mic, "PC")
    ck3 = radiobutton(root, mic, "trust mic")
    mic.set(3)
    # video res
    lab2 = label(root, "Video resolution")
    video = tk.IntVar()
    ck3 = radiobutton(root, video, "Benq monitor")
    ck4 = radiobutton(root, video, "Acer laptop")
    video.set(4)

    # so you can just press enter to start recording
    start = tk.Button(root, text="SPACE TO START", command=root.destroy)
    start.pack()
    start.focus()

    root.mainloop()
    print(mic.get())
    print(video.get())
    # root.bind("<Escape>", print_me)
    return root, mic.get(), video.get()


def record(filename, mic, video):
    # audio = "Microfono (Logitech USB Headset)"
    # audio = "Stereo Mix (Realtek High Definition Audio(SST))"
    # audio = input("Audio 1 (microfono pc) 2 (microfono cuffie)")
    if mic == 1:
        audio = "Microfono (6- Logitech USB Headset)"
    elif mic == 2:
        audio = "Gruppo microfoni (Realtek High Definition Audio(SST))"

    elif mic == 3:
    	audio = "Microfono (USB PnP Sound Device)"
    # audio = "Cuffia auricolare (MAJOR II BLUETOOTH Hands-Free AG Audio)"
    print(f"Using {audio}")
    i = f"-i audio=\"{audio}\""
    # video_size = "1366x768"
    if video == 4:
        video_size = "1680x1050" # monitor
    elif video == 5:
        video_size = "1920x1080" # computer laptop
    
    # added a compressor 15/03/2020
    # Capture both screens
    # i = f"-i video=\"UScreenCapture\":audio=\"{audio}\""
    #Capture one screen
    #screen = "UScreenCapture"
    #screen = "gdigrab"
    screen = "UScreenCapture"

    compressor = "-af acompressor=threshold=0.011623:ratio=9:attack=200:release=1000"
    # compressor = "-af acompressor=threshold=0.011623:ratio=9:attack=200:release=1000:detection=0:makeup=10^^(7.7/20)"
    # compressor = "-af acompressor=threshold=0.089:ratio=9:attack=200:release=1000"
    # compressor = "-af acompressor=threshold=0.031623:ratio=9:attack=200:release=1000"
    # compressor = "-af acompressor=threshold=10^^(-30/20):ratio=9:attack=200:release=1000"
    # compressor = "-af acompressor=threshold=0:ratio=9:attack=200:release=1000"
    # attenuate 10db at 1000 Hz
    # equalizer = "-af \"equalizer=f=1000:width_type=h:width=200:g=-10\""
    # Apply 2 dB gain at 1000 Hz with Q 1 and attenuate 5 dB at 100 Hz with Q 2:
    # equalizer = "-af \"equalizer=f=1000:t=q:w=1:g=2,equalizer=f=100:t=q:w=2:g=-5\""

    #lowpass at 1000
    
    # b0 = -8
    b0 = -4

    # b250 = 4
    b250 = 2

    # e1000 = -8
    e1000 = -6

    e4000 = 0
    e16000 = -8
    equalizer = f"-af \"firequalizer=gain_entry='entry(0,{b0});entry(250,{b250});entry(1000,{e1000});entry(4000,{e4000});entry(16000,{e16000})'\""

    # echo = "-af aecho=1:0.3:10:1"
    # echo = "-af aecho=1.0:0.7:10:0.5"
    echo = ""

    # fr = input("Frame rate (10):")
    fr = 10
    hardware = "-c:v h264_nvenc"
    os.system(f"""ffmpeg -y -rtbufsize 200M -f gdigrab -thread_queue_size 1024 -probesize 10M -r {fr} -draw_mouse 1 -video_size {video_size} -i desktop -f dshow -channel_layout stereo -thread_queue_size 1024 {i} {compressor} {equalizer} -c:v libx264 -r 10 -preset ultrafast -tune zerolatency -crf 25 -pix_fmt yuv420p -c:a aac -strict -2 -ac 2 -b:a 128k -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" {echo} "{filename}" """)


# filename = "rtmp://youtube_stream_url/03r8-71q2-yrvm-bbe7"
# print(get_mic_name())




def mk_bat(cmd):
    command = "py -m " + cmd
    with open(root + cmd + ".bat", "w") as file:
        file.write(command)


# # Create the join.bat program
# command = "py -m joinmp4"
# with open(root + "join.bat", "w") as file:
#     file.write(command)

# create the frame rate program
# mk_bat("joinmp4")
# mk_bat("framerate")



# with open("c:\\users\\giova\\desktop\\ffmpeg_open.bat", "w") as file:
#     file.write("start " + root)

root, mic, video = window()
filepath, file_root = ask()
print(file_root)
record(filepath, mic, video)
# os.startfile("timer.py")

# TO OPEN THE FOLDER 
os.system("start " + filepath + "/" + file_root)

