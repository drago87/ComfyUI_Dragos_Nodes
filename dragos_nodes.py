import math
import glob
import comfy.diffusers_convert
import comfy.samplers
import comfy.sd
import comfy.utils
import comfy.clip_vision
import comfy.model_management
import folder_paths as comfy_paths

def make_comment(checkpoint_name, posetive, negative, width, height, vae_name=None, lora_list=None, info=None):
    text_string = "Checkpoint name: " + checkpoint_name + "\n"
    if  vae_name != None:
        text_string = text_string + "VAE Name: " + vae_name + "\n"
    else:
        text_string = text_string + "VAE Name: Checkpoint VAE\n"
    ##print(text_string)
    if lora_list != None :
        text_string = text_string + "Loras: "
        x = 0
        y = 1
        size = len(lora_list)
        ##print(str(size))
        while x < size:
            if x > 0:
                text_string = text_string + ", "
            text_string = text_string + "Lora"+str(y)+": " + lora_list[x] + ", Strenght: "+str(lora_list[x+1])+", Strenght Clip: "+str(lora_list[x+2])
            ##print(text_string)
            ##print("x: "+str(x)+"\ny: "+str(y))
            
            x=x+3
            y=y+1
            
        text_string = text_string+"\n"
        
    ##print(text_string)
    text_string = text_string + "Seed: "+ str(info.get("Seed: "))
    text_string = text_string + "\nResolution: "+str(width)+"x"+str(height)
    text_string = text_string + "\nSteps: "+str(info.get("Steps: "))+", Start: "+str(info.get("Start at step: "))+", End: "+str(info.get("End at step: "))
    text_string = text_string + "\nCFG: "+str(info.get("CFG scale: "))
    text_string = text_string + "\nSampler: "+str(info.get("Sampler: "))
    text_string = text_string + "\nScheduler: "+str(info.get("Scheduler: "))
    text_string = text_string + "\nDenoising: "+str(info.get("Denoising strength: "))
    text_string = text_string + "\nPosetive Prompts:\n\t"+posetive
    text_string = text_string + "\nNegative Prompts:\n\t"+negative
    #print(text_string)
    return(text_string,)
    
    
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
                }),
                "latents": ("LATENT", {
                    "forceInput": True
                })
            }
        }
    RETURN_TYPES = ("STRING","LATENT")
    RETURN_NAMES = ("Number of Images (as str)","Latent Passtrue")
    
    FUNCTION = "run"
    
    CATEGORY = "DragosNodes"
    
    def run(self, path, padding, latents):
        ##print("init "+str(path))
        if (path[-1]!="/"):
            path = path+"/"
        ##print("after "+ str(path))
        ##print(str(glob.glob(path+"*.png")))
        padding_length=len(glob.glob(path+"*.png"))
        added_padding=len(str(padding_length))
        if padding == 1:
        
            lenght = str(padding_length)
            return(lenght,latents)
        else:
            lenght = ""
            x = 1
            while len(lenght) < added_padding:
                lenght = lenght+"0"
                x+=1
            #print("test " +lenght)
            lenght = lenght + str(padding_length)
            #print(lenght)
            return(lenght,latents)
            
            
    @classmethod       
    def IS_CHANGED(s, latents):
        image_path = folder_paths.get_annotated_filepath(latents)
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        return(float("nan"))
        
class image_info:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "checkpoint_name": ("STRING",{
                    "multiline": False,
                    "forceInput": True
                }),
                "posetive": ("STRING",{
                    "multiline": True,
                    "forceInput": True
                }),
                "negative": ("STRING",{
                    "multiline": True,
                    "forceInput": True
                }),
                "width": ("INT",{
                    "forceInput": True
                }),
                "height": ("INT",{
                    "forceInput": True
                }),
                "top": ("BOOLEAN", {"default": True, "label_on": "Top", "label_off": "Bottom"}),
                "info": ("INFO",{"forceInput": True})
            },
            "optional": {
                "lora_list": ("LIST", {
                    "forceInput": True
                }),
                "extra_info_input": ("STRING",{"forceInput": True}),
                "manual_input": ("STRING",{
                    "multiline": True,
                    "default": ""
                }),
                "vae_name": ("STRING",{"forceInput": True})
            }
                
        }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Image information",)
    
    FUNCTION = "run"
    
    CATEGORY = "DragosNodes"
    
    def run(self, checkpoint_name,  posetive, negative, width, height, info, top, vae_name=None, lora_list=None, extra_info_input=None , manual_input=None):
    
        a = str(extra_info_input)
        b = str(manual_input)
        text_string = "nothing here"
        
        if top == True:
            if b != "":
                text_string = "Manual input: "+ b + "\n\n"
                temp = ''.join(make_comment(checkpoint_name, posetive, negative, width, height,vae_name, lora_list, info))
                text_string = text_string + temp
            else:
                text_string = ''.join(make_comment(checkpoint_name, posetive, negative, width, height,vae_name, lora_list, info))
        else:
            text_string = ''.join(make_comment(checkpoint_name, posetive, negative, width, height,vae_name, lora_list, info))
        #print(text_string)
        
        #print("\na=:"+ a +"\nb=:"+b)

        #print(str(manual_input))
        if top == False:
            if b != "":
                text_string = text_string + "\n\n"+"Manual input: "+ b
        if a != "None":
            text_string = text_string + "\n\n" + a
        
        return(text_string,)
        
class vae_loader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "vae_name": (comfy_paths.get_filename_list("vae"), 
            )}
        }
    RETURN_TYPES = ("VAE","STRING")
    RETURN_NAMES = ("VAE","VAE Name")
    
    FUNCTION = "load_vae"

    CATEGORY = "DragosNodes"

    
    def load_vae(self, vae_name):
        
        vae_path = comfy_paths.get_full_path("vae", vae_name)
        
        sd = comfy.utils.load_torch_file(vae_path)
        #print("sd: "+ str(type(sd) is str))
        vae = comfy.sd.VAE(sd=sd)
        #print("vae: "+ str(type(vae) is str))
        new_vae_name = vae_name.replace(".safetensors","")
        new_vae_name = new_vae_name.replace(".pt","")
        #print(new_vae_name)
        return (vae,new_vae_name)
    
class lora_loader:
    def __init__(self):
        self.loaded_lora = None

    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "model": ("MODEL",),
                              "clip": ("CLIP", ),
                              "lora_name": (comfy_paths.get_filename_list("loras"), ),
                              "strength_model": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
                              "strength_clip": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
                              }}
    RETURN_TYPES = ("MODEL", "CLIP", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("MODEL", "CLIP","lora_name", "strength_model", "strength_clip")
    FUNCTION = "load_lora"

    CATEGORY = "DragosNodes"

    def load_lora(self, model, clip, lora_name, strength_model, strength_clip):
        if strength_model == 0 and strength_clip == 0:
            return (model, clip)

        lora_path = comfy_paths.get_full_path("loras", lora_name)
        lora = None
        if self.loaded_lora is not None:
            if self.loaded_lora[0] == lora_path:
                lora = self.loaded_lora[1]
            else:
                temp = self.loaded_lora
                self.loaded_lora = None
                del temp

        if lora is None:
            lora = comfy.utils.load_torch_file(lora_path, safe_load=True)
            self.loaded_lora = (lora_path, lora)

        model_lora, clip_lora = comfy.sd.load_lora_for_models(model, clip, lora, strength_model, strength_clip)
        return_lora_name = lora_name.replace(".safetensors","")
        return (model_lora, clip_lora,return_lora_name,str(strength_model),str(strength_clip))

        
NODE_CLASS_MAPPINGS = {
    "file_padding": file_padding,
    "image_info": image_info,
    "vae_loader": vae_loader,
    "lora_loader": lora_loader
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "file_padding": "File Padding",
    "image_info": "Image Info",
    "vae_loader": "VAE Loader With Name",
    "lora_loader": "Lora Loader with info"
}