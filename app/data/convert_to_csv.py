import pandas as pd
import os

dirs_to_check = [dir for dir in os.listdir(os.getcwd())
 if os.path.isdir(dir)]

for dir_name in dirs_to_check:
    x = os.walk("./"+dir_name)
    current_files = next(x)[2]
    for file in current_files:
        
        file_name, ext = file.split(".")
        
        if ext=="xlsx":
            df = pd.read_excel(f"./{dir_name}/{file}")
            df.to_csv(f"./{dir_name}/{file_name}.csv", index=False)
            os.remove(f"./{dir_name}/{file_name}.xlsx") 