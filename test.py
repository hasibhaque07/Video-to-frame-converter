import cv2
import os
from tkinter import filedialog, Tk, Button, Label, OptionMenu, StringVar, IntVar

def select_video():
    global video_path
    video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
    video_label.config(text=f"Video: {video_path}")

def select_destination():
    global destination_folder
    destination_folder = filedialog.askdirectory()
    destination_label.config(text=f"Destination: {destination_folder}")

def convert_video():
    if not video_path or not destination_folder:
        print("Please select a video and destination folder")
        return

    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    frame_interval = frame_interval_var.get()
    output_format = output_format_var.get()

    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % frame_interval == 0:
            frame_name = os.path.join(destination_folder, f"frame_{count}.{output_format}")
            cv2.imwrite(frame_name, frame)
        count += 1

    cap.release()
    print("Conversion completed")

# GUI setup
root = Tk()
root.title("Video to Frames Converter")

video_path = ""
destination_folder = ""

video_label = Label(root, text="Video: Not selected")
video_label.pack()

select_video_button = Button(root, text="Select Video", command=select_video)
select_video_button.pack()

destination_label = Label(root, text="Destination: Not selected")
destination_label.pack()

select_destination_button = Button(root, text="Select Destination", command=select_destination)
select_destination_button.pack()

frame_interval_var = IntVar(value=10)
frame_interval_label = Label(root, text="Select Frame Interval")
frame_interval_label.pack()
frame_interval_menu = OptionMenu(root, frame_interval_var, 1, 5, 10, 20, 30, 60)
frame_interval_menu.pack()

output_format_var = StringVar(value="jpg")
output_format_label = Label(root, text="Select Output Format")
output_format_label.pack()
output_format_menu = OptionMenu(root, output_format_var, "jpg", "png")
output_format_menu.pack()

convert_button = Button(root, text="Start Converting", command=convert_video)
convert_button.pack()

root.mainloop()