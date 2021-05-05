import json

def read_img_settings():
    try:
        pic_config = open("pic_config.json", "r")

        config_readings = json.loads(pic_config.read())

        pic_config.close()

        return config_readings
    
    except FileNotFoundError:
        print("cant open teh file")

def save_img_settings(threshold,kernel_config):
    try:
        pic_config = open("pic_config.json", "w")
        pic_config.write(json.dumps({"threshold": threshold, "kernel_config": kernel_config}))
        pic_config.close()
    
    except FileNotFoundError:
        print("cant open teh file")