import math
import glob

class file_padding:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path": ("STRING",{
                    "multiline": False,
                    "default": "./ComfyUI/output/"
                }),
                "padding": ("INT", {
                    "default": 4,
                    "min": 1,
                    "max": 10,
                    "step": 1,
                    "display": "number"
                })
            }
        }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Number of Images (as str)",)
    
    FUNCTION = "run"
    
    CATEGORY = "DragosNodes"
    
    def run(self, path, padding):
        #print("init "+str(path))
        if (path[-1]!="/"):
            path = path+"/"
        #print("after "+ str(path))
        #print(str(glob.glob(path+"*.png")))
        if padding == 1:
        
            lenght = str(len(glob.glob(path+"*.png")))
            return(lenght)
        else:
            lenght = ""
            x = 1
            while x < padding:
                lenght = lenght+"0"
                x+=1
            print("test " +lenght)
            lenght = lenght + str(len(glob.glob(path+"*.png")))
            print(lenght)
            return(lenght)
     
NODE_CLASS_MAPPINGS = {
    "file_padding": file_padding
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "file_padding": "File Padding"
}