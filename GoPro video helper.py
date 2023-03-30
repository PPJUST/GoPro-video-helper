# gopro

```python
import os

def rename_gopro_all():
    path = "./"
    count = 0
    file_list = os.listdir(path)  # 遍历路径
    print (file_list)
    for file in file_list:  # 遍历文件
        if 'GH' in file:  # 检查“GH”字符串
            olddir = os.path.join(path,file)
            if os.path.isdir(olddir):
                continue
            filename = os.path.splitext(file)[0] # 提取文件名
            filetype = os.path.splitext(file)[1].upper() # 提取后缀

# GH010320
            if filetype in [".MP4",".JPG",".LRV",".THM"] and filename[0]=="G" and "_" not in filename:
                NAME_PREFIX = filename[:2] # GH
                NAME_INDEX = filename[2:4] # 01
                NAME_SEQ = filename[4:] # 0320
                newdir = os.path.join(path, NAME_PREFIX + NAME_SEQ + "_" + NAME_INDEX + filetype.lower())
# GH0320_01
                print (newdir)
                os.rename(olddir,newdir)
                count +=1

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    rename_gopro_all ()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
```

改名为文件日期-视频组

是否合并视频

GOPRO7文件名规则

GH010320

01为顺序，0320为组

实际视频顺序：GH0320_01

GORPO5规则

GOPROxxxx开头的是第一段，GP01xxxx的是后续，最后四位xxxx一样的为同一段视频，01为顺序编号，4G一个视频
