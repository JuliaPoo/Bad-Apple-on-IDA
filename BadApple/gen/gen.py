import _image, _movie

def gen(filepath:str, width:int, height:int):
    _image.gen(width, height)
    _movie.gen(filepath, width, height)

if __name__=="__main__":
    width, height, filepath = int(input("Width: ")), int(input("Height: ")), input("Filepath: ")
    gen(filepath, width, height)
    print("Wrote to `movie.cpp`, `image.cpp` and `image.h`")