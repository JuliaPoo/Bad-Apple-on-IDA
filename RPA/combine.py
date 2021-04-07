import cv2
import os

image_folder = 'out'

images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
images = sorted(images, key=lambda f: int(f[5:-4]))

frame = cv2.imread(os.path.join(image_folder, images[0]))

ymi,yma = 20,-40
frame = frame[ymi:yma,:]

height, width, layers = frame.shape

video = cv2.VideoWriter(
    'rsrc/IDA-BadApple.mp4', 
    fourcc=cv2.VideoWriter_fourcc(*'MP4V'), 
    frameSize=(width, height), 
    fps=15*2
)

for idx,image in enumerate(images):
    frame = cv2.imread(os.path.join(image_folder, image))[ymi:yma,:]
    video.write(frame)
    video.write(frame)
    print("Frame %s\r"%image, end="")

cv2.destroyAllWindows()
video.release()

from moviepy.editor import VideoFileClip, CompositeVideoClip

clip0 = VideoFileClip("../BadApple/gen/rsrc/BadApple.mp4")
clip1 = VideoFileClip("rsrc/IDA-Start.mp4")
clip2 = VideoFileClip("rsrc/IDA-BadApple.mp4")

composite = CompositeVideoClip([clip2, clip0.resize(.5).set_position((65,700))])
final_clip = CompositeVideoClip([clip1, composite.set_start(12)])
final_clip.write_videofile("final.mp4", fps=30)