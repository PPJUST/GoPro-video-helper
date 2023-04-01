import os
import time
import subprocess
import shutil


def get_path():
    """获取文件夹路径"""
    file_path = input('★★★输入GoPro视频所在文件夹： ')
    if os.path.exists(file_path) and os.path.isdir(file_path):
        walk_path(file_path)
    else:
        print('——————文件夹不存在——————')
        get_path()


def ask_merge(video_group_copy):
    """合并视频"""
    ask = input('★★★是否合并视频（Y/N）： ')
    if ask.upper() == 'Y':
        key_total = len(video_group_copy)
        key_number = 0
        for key in video_group_copy:
            key_number += 1
            inputfiles_write = ""
            for i in sorted(video_group_copy[key]):
                inputfiles_write += "file '" + i + "'\n"
            with open('inputfiles.txt', 'w', encoding='utf-8') as iw:
                iw.write(inputfiles_write)
            time.sleep(0.1)  # 测试
            output_file = key
            command = f"ffmpeg -f concat -safe 0 -i inputfiles.txt -c copy {output_file}"
            subprocess.run(command)
            print(f'——————已完成第{key_number}组视频合并，共{key_total}组——————')
            os.remove('inputfiles.txt')
            # 移动文件到文件夹
            os.mkdir(os.path.splitext(key)[0])
            for i in sorted(video_group_copy[key]):
                shutil.move(i, os.path.splitext(key)[0])
        print('——————已完成全部视频合并，并将分段视频移至单独文件夹——————')
    elif ask.upper() == 'N':
        pass
    else:
        print('——————输入不正确——————')
        ask_merge(video_group_copy)


def walk_path(path):
    """遍历文件"""
    files = os.listdir(path)
    full_files = []
    for i in files:
        full_files.append(os.path.join(path, i))
    video_files = []
    # 提取mp4后缀的文件
    for i in full_files:
        if os.path.isfile(i) and os.path.splitext(i)[1].upper() == '.MP4':
            video_files.append(i)  # 提取出mp4后缀的文件
    select_mode(video_files)


def select_mode(files):
    """修改文件名"""
    '''
    GoPro7文件名规则：
    例如：GH010320.mp4，GH010321.mp4，GH020320.mp4
    GH 为固定前缀，01 为视频组的第1个视频，0320 为视频编号，视频编号相同的为同一组视频
    
    GoPro5文件名规则：
    例如：GOPR1024.mp4，GP011024.mp4，GP021024.mp4
    GOPR 开头的为视频组的第1个视频，1024 为视频编号，视频编号相同的为同一组视频，后续GP01为顺序编号
    '''
    check_first_file = os.path.split(files[0])[1]  # 提取第一个文件名
    if check_first_file.find('GH') != -1:
        run_rename(files, 'gopro7')
    elif check_first_file.find('GOPR') != -1 or check_first_file.find('GP') != -1:
        run_rename(files, 'gopro5')
    else:
        pass  # 占位，不清楚其他型号的命名规则


def run_rename(files, gopro_mode):
    """修改文件名"""
    video_group = {}  # 存放最终分类结果，key编号1024-value完整文件名
    for file in files:
        if get_filename(file)[-4:] not in video_group:  # 如果字典中没有该项，则添加空列表项
            video_group[get_filename(file)[-4:]] = []
        video_group[get_filename(file)[-4:]].append(file)
    video_group_copy = {}  # 用于合并视频的复制字典
    for key in video_group:
        new_name_path = os.path.split((sorted(video_group[key])[0]))[0]
        new_name_group = str(key)
        new_name_time = os.path.getmtime(sorted(video_group[key])[0])
        new_name_time = time.gmtime(new_name_time)  # 标准化时间
        new_name_time = time.strftime("%Y%m%d-%H.%M.%S", new_name_time)  # 格式化时间
        new_name_prefix = 'GoPro'
        new_name_suffix = os.path.splitext((sorted(video_group[key])[0]))[1]
        for value in sorted(video_group[key]):
            if gopro_mode == "gopro7":
                new_name_number = get_filename(value)[-6:-4]
            elif gopro_mode == "gopro5":
                if value.find('GOPR') != -1:
                    new_name_number = '01'
                else:
                    new_name_number = "{:02d}".format(int(get_filename(value)[-6:-4]) + 1)
            new_name = new_name_prefix + '_' + new_name_time + '_' + new_name_group + '_' + new_name_number + new_name_suffix
            new_full_name = os.path.join(new_name_path, new_name)
            os.rename(value, new_full_name)

            new_key = os.path.join(new_name_path, new_name_time + '_' + new_name_group + new_name_suffix)
            if new_key not in video_group_copy:
                video_group_copy[new_key] = []
            video_group_copy[new_key].append(new_full_name)
    print('——————全部视频已改名——————')
    ask_merge(video_group_copy)


def get_filename(x):
    """提取文件名"""
    return os.path.splitext(os.path.split(x)[1])[0]


def hello():
    word = '''
使用步骤：
1. 输入GoPro视频所在文件夹路径，程序会自动改名。
改名格式为“GoPro_拍摄日期-时间_内部编号_第几个视频”，示例GoPro_20230101-12.50.05_0021_01.mp4

2. 改名完成后可以选择合并视频，合并方法为调用ffmpeg无损合并。
合并完成后，分段视频将会保存到单独的文件夹中。
如果程序内没有ffmpeg.exe请自行下载。
        '''
    print(word)


def main():
    hello()
    get_path()


if __name__ == "__main__":
    main()
