import cv2
import numpy as np

def _gen_movie(filepath:str, width:int, height:int):

    vidcap = cv2.VideoCapture(filepath)
    success, img = vidcap.read()
    count = 0
    frames = []
    while success:
        
        if count%2 == 0: # 30fps to 15fps
            img = cv2.resize(img, dsize=(width, height), interpolation=cv2.INTER_CUBIC)
            frames.append(img)
            #cv2.imwrite(out+r"\frame%d.jpg" % (count//3), img)
            print("Frame %d\r"%count, end="")
            
        count += 1
        success, img = vidcap.read() 

    diffs = []
    frames = [np.array(np.array(f[:,:,0], dtype=np.float) * 23/255, dtype=np.uint8) for f in frames]
    frames = [np.ones((height, width), dtype=np.uint8)*23] + frames

    for i,f in enumerate(frames[1:]):
        fp, fc = frames[i-1],f
        d = []
        for x in range(width):
            for y in range(height):
                if fp[y,x] == fc[y,x]:
                    continue
                d.append((x,y,fc[y,x]))
        diffs.append((len(d), d))

    string = ["#include \"../pixels.h\"", ""]
    for idx,(nd,d) in enumerate(diffs[1:]):
        if nd:
            string.append("char frame%d[] = {%s};"%(idx, ",".join(str(j) for i in d for j in i)))
        else:
            string.append("char* frame%d;"%idx)

    movie = "FRAME movie[] = {%s};"%(",".join("{%d,%s}"%(nd, "frame%d"%idx) for idx,(nd,_) in enumerate(diffs[1:])))
    string.extend(["", movie, "int n_frames = sizeof(movie) / sizeof(FRAME);"])

    return "\n".join(string)

def gen(filepath:str, width:int, height:int):
    open("movie.cpp", "w").write(_gen_movie(filepath, width, height))

if __name__ == "__main__":
    width, height, filepath = int(input("Width: ")), int(input("Height: ")), input("Filepath: ")
    gen(filepath, width, height)
    print("Wrote to `movie.cpp`")