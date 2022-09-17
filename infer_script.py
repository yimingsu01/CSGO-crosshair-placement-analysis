import os
import re
import time

import cv2
import math
import glob
from PIL import Image
import moviepy.video.io.ImageSequenceClip
import argparse


def FindFrameByID(target_id, frame_files):
    for filename in frame_files:
        splitted = filename.replace(".png", "").split("_")
        frame_id = splitted[0]
        if target_id == frame_id:
            print(f"[INFO] found frame {filename} by id {target_id}")
            return filename
    print(f"[INFO] frame {filename} not found, skipping...")
    return -1


def dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx**2 + dy**2)


def Visualize(pred_path, frame_path, output_path, video_filename):
    total_dist = 0
    pred_files = os.listdir(pred_path)
    frame_files = os.listdir(frame_path)
    print(f"pred_path: {os.listdir(pred_path)}")
    print(f"frame_path: {os.listdir(frame_path)}")

    count = 0
    for filename in pred_files:
        splitted1 = filename.replace(".txt", "").split("_")
        frame_id = splitted1[1]
        frame_filename = FindFrameByID(frame_id, frame_files)
        raw_pred_string = ""

        with open(pred_path+filename, "r") as pred_text:
            raw_pred_string = pred_text.readline()
            raw_pred_string = raw_pred_string.replace("\n", "")

        prediction = raw_pred_string.split(" ")
        label = "body"
        x1 = int(prediction[1])
        y1 = int(prediction[2])
        x2 = int(prediction[3])
        y2 = int(prediction[4])
        conf = float(prediction[5])

        screen_center = (1920 // 2, 1080 // 2)
        bbox_center = ((x1+x2) // 2, (y1+y2) // 2)
        ch_dist = dist(screen_center, bbox_center)
        total_dist += ch_dist

        print(f"[INFO] p1: {bbox_center}, p2: {screen_center}, conf: {conf}")
        print(f"[INFO] dist in px: {ch_dist}")

        frame = cv2.imread(frame_path+frame_filename)
        cv2.line(frame, bbox_center, screen_center, (0, 255, 0), 2)

        write_filename = str(count)+".png"
        # cv2.imshow("0", frame)
        cv2.imwrite(output_path+write_filename, frame)
        count += 1

    total_dist = total_dist / len(pred_files)
    with open(video_filename+"_result.txt", "w") as f:
        print(f"[RES] average distance from target: {int(total_dist)}", file=f)


def OutputToGif(output_path, filename):
    frames = []
    imgs = glob.glob(output_path + "*.png")
    imgs.sort(key=lambda f: int(re.sub('\D', '', f)))
    # print(imgs)
    for i in imgs:
        new_frame = Image.open(i)
        frames.append(new_frame)

    print("[INFO] Converting the png predictions to a gif file")
    # Save into a GIF file that loops forever
    frames[0].save(f'{filename}_result.gif', format='GIF',
                   append_images=frames[1:],
                   save_all=True,
                   duration=200, loop=0)


def OutputToVideo(output_path, filename):
    frames = []
    imgs = glob.glob(output_path + "*.png")
    imgs.sort(key=lambda f: int(re.sub('\D', '', f)))
    # print(imgs)
    for i in imgs:
        new_frame = Image.open(i)
        frames.append(new_frame)

    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(imgs, fps=25)
    clip.write_videofile(f"{filename}_result.mp4")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--video', type=str, help='video path')
    parser.add_argument('--weights', type=str, help='weight path')
    parser.add_argument('--label', type=str, help='labels path')
    parser.add_argument('--frame', type=str, help='frame path')
    parser.add_argument('--annotated', type=str, help='path to image annotated')


    arg = parser.parse_args()
    video_filename = arg.video
    video_name = video_filename.split(".")[0]

    command = f"python detect.py --weights {arg.weights} --conf 0.6 --source {video_filename} --save-conf --save-txt" \
              f" --name {video_name}"

    os.system(command)

    Visualize(arg.label, arg.frame, arg.annotated, video_name)
    OutputToGif(arg.annotated, video_name)
    OutputToVideo(arg.annotated, video_name)