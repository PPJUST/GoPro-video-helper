# gopro

import os, time, subprocess




'''

改名为文件日期-视频组

是否合并视频

GOPRO7文件名规则

GH010320

01为顺序，0320为组

实际视频顺序：GH0320_01

GORPO5规则

GOPROxxxx开头的是第一段，GP01xxxx的是后续，最后四位xxxx一样的为同一段视频，01为顺序编号，4G一个视频

目前思路：1.给出路径，遍历文件，检查后缀和文件名 2.对文件编号 3. 是否合并视频>>>如果合并，则将视频组放到一个文件夹中，外部只留合并后的视频文件

'''
is_merge = False  # 是否合并，默认否

def get_path():
    '''获取文件夹路径'''
    file_path = input('输入GoPro视频所在文件夹：')
    if os.path.exists(file_path) and os.path.isdir(file_path):
        walk_path(file_path)
    else:
        print('文件夹不存在')
        get_path()
def ask_merge():
    ask = input('是否合并视频 Y/N')
    global is_merge
    if ask == 'Y':
        is_merge = True
    elif ask == 'N':
        is_merge = False

def walk_path(path):
    '''遍历文件'''
    files = os.listdir(path)
    full_files = []
    for i in files:
        full_files.append(os.path.join(path, i))
    video_files = []
    # 提取mp4后缀的文件
    for i in full_files:
        if os.path.isfile(i) and os.path.splitext(i)[1].upper() == '.MP4':
            video_files.append(i)  # 提取出mp4后缀的文件
    rename_files(video_files)

def rename_files(files):
    '''修改文件名'''
    '''
    GoPro7文件名规则：
    例如：GH010320.mp4，GH010321.mp4，GH020320.mp4
    GH 为固定前缀，01 为视频组的第1个视频，0320 为视频编号，视频编号相同的为同一组视频
    
    GoPro5文件名规则：
    例如：GOPRO1024.mp4，GP011024.mp4，GP021024.mp4
    GOPRO 开头的为视频组的第1个视频，1024 为视频编号，视频编号相同的为同一组视频，后续GP01为顺序编号
    '''
    check_first_file = os.path.split(files[0])[1]  # 提取第一个文件名
    if check_first_file.find('GH') != -1:
        rule_gopro7(files)
    elif check_first_file.find('GOPRO') != -1 or check_first_file.find('GP') != -1:
        rule_gopro5(files)
    else:
        pass  # 占位，不清楚其他型号的命名规则

def rule_gopro7(files):
    '''GoPro7重命名规则'''
    # 命名思路：1.文件名后四位放到集合中，得到所有视频组编号 2.创建字典，key为视频组编号，value为视频分卷路径
    '''
    GoPro7文件名规则：
    例如：GH010320.mp4，GH010321.mp4，GH020320.mp4
    GH 为固定前缀，01 为视频组的第1个视频，0320 为视频编号，视频编号相同的为同一组视频
    '''
    video_number = set()
    video_group = {}  # 存放最终分类结果，key编号1024-value完整文件名

    def get_filename(x):
        return os.path.splitext(os.path.split(x)[1])[0]

    for file in files:
        if get_filename(file)[-4:] not in video_group:  # 如果字典中没有该项，则添加空列表项
            video_group[get_filename(file)[-4:]] = []
        video_group[get_filename(file)[-4:]].append(file)
    video_group_copy = {}  # 用于合并视频的复制字典
    for key in video_group:
        new_name = ''
        new_name_path = os.path.split((sorted(video_group[key])[0]))[0]
        new_name_group = str(key)
        new_name_time = os.path.getmtime(sorted(video_group[key])[0])
        new_name_time = time.gmtime(new_name_time)  # 标准化时间
        new_name_time = time.strftime("%Y-%m-%d %H-%M-%S", new_name_time)  # 格式化时间
        new_name_suffix = os.path.splitext((sorted(video_group[key])[0]))[1]
        for value in sorted(video_group[key]):
            new_name_number = get_filename(value)[-6:-4]
            new_name = new_name_time + '_' + new_name_group + '_' + new_name_number + new_name_suffix
            new_full_name = os.path.join(new_name_path, new_name)
            print(f'原文件名{value}')
            print(f'新文件名{new_full_name}')
            os.rename(value, new_full_name)

            new_key = os.path.join(new_name_path, new_name_time + '_' + new_name_group + new_name_suffix)
            if new_key not in video_group_copy:
                video_group_copy[new_key] = []
            video_group_copy[new_key].append(new_full_name)
    print(video_group_copy)
    ask_merge()
    if is_merge:
        for key in video_group_copy:
            input_files = "|".join(sorted(video_group_copy[key]))
            print(input_files)
            output_file = key
            ffmepg_path = 'ffmpeg.exe'
            command = f'{ffmepg_path} -i "concat:{input_files}" -c copy "{output_file}"'
            run_merge = subprocess.run(command)


def rule_gopro5(files):
    '''GoPro5重命名规则'''
    '''
    GoPro5文件名规则：
    例如：GOPRO1024.mp4，GP011024.mp4，GP021024.mp4
    GOPRO 开头的为视频组的第1个视频，1024 为视频编号，视频编号相同的为同一组视频，后续GP01为顺序编号
    '''
    video_number = set()
    video_group = {}  # 存放最终分类结果，key编号1024-value完整文件名
    def get_filename(x):
        return os.path.splitext(os.path.split(x)[1])[0]

    for file in files:
        if get_filename(file)[-4:] not in video_group:  # 如果字典中没有该项，则添加空列表项
            video_group[get_filename(file)[-4:]] = []
        video_group[get_filename(file)[-4:]].append(file)
    video_group_copy = {}  # 用于合并视频的复制字典
    for key in video_group:
        new_name = ''
        new_name_path = os.path.split((sorted(video_group[key])[0]))[0]
        new_name_group = str(key)
        new_name_time = os.path.getmtime(sorted(video_group[key])[0])
        new_name_time = time.gmtime(new_name_time)  # 标准化时间
        new_name_time = time.strftime("%Y-%m-%d %H-%M-%S", new_name_time)  # 格式化时间
        new_name_suffix = os.path.splitext((sorted(video_group[key])[0]))[1]
        for value in sorted(video_group[key]):
            if value.find('GOPRO') != -1:  # 相比gopro7规则代码不同的地方
                new_name_number = 0
            else:
                new_name_number = get_filename(value)[-6:-4] + 1
            new_name = new_name_time + '_' + new_name_group + '_' + new_name_number + new_name_suffix
            new_full_name = os.path.join(new_name_path, new_name)
            print(f'原文件名{value}')
            print(f'新文件名{new_full_name}')
            os.rename(value, new_full_name)

            new_key = os.path.join(new_name_path, new_name_time + '_' + new_name_group + new_name_suffix)
            if new_key not in video_group_copy:
                video_group_copy[new_key] = []
            video_group_copy[new_key].append(new_full_name)
    print(video_group_copy)
    ask_merge()
    if is_merge:
        for key in video_group_copy:
            input_files = "|".join(sorted(video_group_copy[key]))
            print(input_files)
            output_file = key
            ffmepg_path = 'ffmpeg.exe'
            command = f'{ffmepg_path} -i "concat:{input_files}" -c copy "{output_file}"'
            run_merge = subprocess.run(command)




def rule_gopromax(files):
    '''GoPro Max重命名规则'''
    pass



get_path()

'''
GOPRO7文件名规则



目前思路：1.给出路径，遍历文件，检查后缀和文件名 2.对文件编号 3. 是否合并视频>>>如果合并，则将视频组放到一个文件夹中，外部只留合并后的视频文件
'''

