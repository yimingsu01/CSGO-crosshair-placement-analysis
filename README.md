# CSGO-crosshair-placement-analysis
This is a repo of csgo crosshair placement (or misplacement) analysis using yolov7's object detection.

![gif](img/out.gif)

## Prerequisite
You will need to make a conda environment and install the packages in `requirements.txt`. 
Notice that `requirements.txt` is not made for `pip`, but conda. Inside the txt file there are instructions to how to install it with conda.

You need to have [yolov7](https://github.com/WongKinYiu/yolov7) cloned first.
Your `yolov7` folder is your root folder for this repo to work.

Copy `inference.py` and `infer_script.py` to your root folder.

`inference.py` is for debugging and `infer_script.py` is for running in terminal with arguments.

You will need a video file of your gameplay that you want to analyze, and a `yolov7` weight. I have provided one `best.pt` that 
I trained on personal dataset. This weight file works the best when provided a mirage gameplay.

## Usage
First, you will need to replace `yolov7`'s training script with the one in this repo. The only change is
to save a corresponding frame with every prediction saved in txt. You can also add this line by yourself
```
cv2.imwrite(f'path/to/frame/{frame}_{(int(time.time()))}.png', im0)
```
after `plot_one_box` function in `detect.py`. You can change the `path/to/frame/` to any folder you want.
This saves frames for us to analyze that, when detected a body in the frame, what's the distance from the target to the crosshair.

Then you will need to find where `yolov7` saves the label predictions in txt. It's usually in `run/detect/the_name_of_your_video/labels`, without file extension.

You will need to provide a folder to save the annotated images temporarily, so they can be converted to GIF and mp4 video.

Arguments:
 - `--video` path to video file
 - `--weights` path to model weights
 - `--label` path to labels provided by yolov7
 - `--frame` path to frame saved by yolov7.`detect.py`
 - `--annotated` path to folder that saves the annotated images, should be empty

After running `infer_script.py`, there should be three files:
 - `video_name_result.txt` the average distance from your crosshair to targets
 - `video_name_result.gif` a gif file that visualizes the distances
 - `video_name_result.mp4` same as above but in mp4.

## Acknowledgement
Thanks to author and researcher that published `yolov7` on Github to make this repo is possible.
