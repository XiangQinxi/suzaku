import sys
import ctypes
import sdl2dll              # 导入pysdl2-dll
from sdl2 import *          # 导入pysdl2
from sdl2.sdlimage import * # 加载图片需要，否则只能加载BMP

def main():
    SDL_Init(SDL_INIT_VIDEO)
    IMG_Init(IMG_INIT_JPG)
    window = SDL_CreateWindow(b"Hello World",
                              SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
                              592, 460, SDL_WINDOW_SHOWN |SDL_WINDOW_RESIZABLE)
    windowsurface = SDL_GetWindowSurface(window)

    image = IMG_Load(b"exampleimage.jpg")
    rect = SDL_Rect(0,0,0,0)
    SDL_BlitSurface(image, None, windowsurface, rect)

    #SDL_RenderCopyEx(window,image,None,None,90.0,SDL_Point(0,0),SDL_FLIP_NONE)
    cur = SDL_Cursor()
    cur =  SDL_CreateSystemCursor(SDL_SYSTEM_CURSOR_HAND)
    sur = SDL_Surface()
    cur = SDL_CreateColorCursor(image,0,0)
    SDL_SetCursor(cur)

    SDL_UpdateWindowSurface(window)
    SDL_FreeSurface(image)

    running = True
    event = SDL_Event()
    while running:
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_QUIT:
                running = False
                break

    SDL_DestroyWindow(window)
    SDL_Quit()
    return 0

if __name__ == "__main__":
    sys.exit(main())

