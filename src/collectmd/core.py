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
    # 原来 process_csv_file 函数的内容移到这里
    # 保持原有逻辑不变，但改为更模块化的形式
    pass 