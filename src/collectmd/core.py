import os
import csv
import shutil
from datetime import datetime

def process_efu_file(file_path, target_dir):
    """
    处理 EFU 文件并移动相关文件到目标目录
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"源文件不存在: {file_path}")
        
    if not os.path.exists(target_dir):
        raise FileNotFoundError(f"目标目录不存在: {target_dir}")
    
    try:
        _process_csv_file(file_path, target_dir, 'utf-8')
    except UnicodeDecodeError:
        _process_csv_file(file_path, target_dir, 'gbk')

def _process_csv_file(file_path, target_dir, encoding):
    """处理 CSV 文件并移动相关文件到目标目录"""
    with open(file_path, 'r', encoding=encoding) as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # 读取表头
        print(f"CSV 表头: {header}")
        
        row_count = 0
        for row in csv_reader:
            row_count += 1
            print(f"\n处理第 {row_count} 行: {row}")
            
            # 跳过空行或无效行
            if not row or len(row) == 0:
                print("跳过空行")
                continue
                
            source_dir = row[0].strip()
            if not source_dir:
                print("源路径为空，跳过")
                continue
                
            if not os.path.exists(source_dir):
                print(f"源文件夹不存在: {source_dir}")
                continue
                
            if not os.path.isdir(source_dir):
                print(f"不是文件夹，跳过: {source_dir}")
                continue

            # 处理源文件夹下的所有文件
            for root, dirs, files in os.walk(source_dir):
                # 处理 images 文件夹
                if 'images' in dirs:
                    _process_images_folder(root, target_dir)

                # 处理所有文件
                for file in files:
                    _process_single_file(root, file, target_dir)
            
            # 清理空文件夹
            try:
                shutil.rmtree(source_dir)
                print(f"已清理源文件夹: {source_dir}")
            except Exception as e:
                print(f"清理源文件夹失败: {str(e)}")
        
        print(f"\n总共处理了 {row_count} 行数据")

def _process_images_folder(root, target_dir):
    """处理 images 文件夹"""
    images_dir = os.path.join(root, 'images')
    target_images = os.path.join(target_dir, 'images')
    try:
        print(f"正在移动 images 文件夹: {images_dir} -> {target_images}")
        if not os.path.exists(target_images):
            os.makedirs(target_images)
        for img in os.listdir(images_dir):
            src_img = os.path.join(images_dir, img)
            dst_img = os.path.join(target_images, img)
            shutil.copy2(src_img, dst_img)
            os.remove(src_img)
        os.rmdir(images_dir)
        print(f"已成功移动 images 文件夹")
    except Exception as e:
        print(f"移动 images 文件夹失败: {str(e)}")

def _process_single_file(root, file, target_dir):
    """处理单个文件"""
    source_path = os.path.join(root, file)
    target_path = os.path.join(target_dir, file)
    
    # 处理 md 文件
    if file.lower().endswith('.md'):
        if os.path.exists(target_path):
            # 如果 md 文件已存在，记录到 same.log
            log_path = os.path.join(target_dir, 'same.log')
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(log_path, 'a', encoding='utf-8') as log:
                log.write(f"{current_time} - {source_path}\n")
            print(f"MD文件已存在，已记录到日志: {source_path}")
            return
    
    # 移动所有非 md 文件或不存在于目标目录的 md 文件
    try:
        print(f"正在移动文件: {source_path} -> {target_path}")
        shutil.copy2(source_path, target_path)
        os.remove(source_path)
        print(f"已成功移动: {source_path} -> {target_path}")
    except Exception as e:
        print(f"移动失败 {source_path}: {str(e)}")