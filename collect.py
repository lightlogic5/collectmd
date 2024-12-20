import os
import csv
import shutil
from datetime import datetime

def read_efu_file():
    # 获取桌面路径
    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    file_path = os.path.join(desktop, os.getenv('EFU_PATH', 'aa.efu'))
    
    # 获取目标路径
    target_dir = os.getenv('ALL_MD_PATH')
    print("============",target_dir)
    if not target_dir:
        print("错误: 未设置 ALL_MD_PATH 环境变量")
        return
        
    print(f"尝试读取文件: {file_path}")
    print(f"目标路径: {target_dir}")
    
    # 检查源文件是否存在
    if not os.path.exists(file_path):
        print(f"错误: 源文件 {file_path} 不存在")
        return
        
    # 检查目标目录是否存在
    if not os.path.exists(target_dir):
        print(f"错误: 目标目录 {target_dir} 不存在")
        return
    
    # 使用 csv 模块读取
    try:
        print("\n=== 使用 csv 模块读取并移动文件 ===")
        process_csv_file(file_path, target_dir, 'utf-8')
    except UnicodeDecodeError:
        # UTF-8 编码失败时尝试 GBK 编码
        try:
            process_csv_file(file_path, target_dir, 'gbk')
        except Exception as e:
            print(f"GBK 编码读取失败: {str(e)}")
    except Exception as e:
        print(f"CSV 读取失败: {str(e)}")

def process_csv_file(file_path, target_dir, encoding):
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

            # 用于标记是否有md文件因重名而未移动
            has_unmoved_md = False

            # 处理源文件夹下的所有文件
            for root, dirs, files in os.walk(source_dir):
                # 移动所有非md文件和文件夹
                for dir_name in dirs:
                    source_path = os.path.join(root, dir_name)
                    target_path = os.path.join(target_dir, dir_name)
                    try:
                        if os.path.exists(target_path):
                            shutil.rmtree(target_path)
                        shutil.copytree(source_path, target_path)
                        shutil.rmtree(source_path)
                        print(f"已成功移动文件夹: {source_path} -> {target_path}")
                    except Exception as e:
                        print(f"移动文件夹失败: {source_path}")
                        error_log_path = os.path.join(target_dir, 'error.log')
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        with open(error_log_path, 'a', encoding='utf-8') as log:
                            log.write(f"{current_time} - {source_path}: {str(e)}\n")

                # 处理所有文件
                for file_name in files:
                    source_path = os.path.join(root, file_name)
                    target_path = os.path.join(target_dir, file_name)
                    
                    try:
                        if file_name.lower().endswith('.md'):
                            # 检查目标目录中是否存在同名md文件
                            target_md_files = [f for f in os.listdir(target_dir) if f.lower().endswith('.md')]
                            if file_name in target_md_files:
                                # 记录到same.log
                                same_log_path = os.path.join(target_dir, 'same.log')
                                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                with open(same_log_path, 'a', encoding='utf-8') as log:
                                    log.write(f"{current_time} - {source_path}\n")
                                print(f"MD文件已存在，已记录到日志: {source_path}")
                                has_unmoved_md = True
                                continue
                            else:
                                # 移动md文件
                                shutil.copy2(source_path, target_path)
                                os.remove(source_path)
                                print(f"已成功移动文件: {source_path} -> {target_path}")
                        else:
                            # 移动非md文件
                            shutil.copy2(source_path, target_path)
                            os.remove(source_path)
                            print(f"已成功移动文件: {source_path} -> {target_path}")
                    except Exception as e:
                        print(f"移动文件失败: {source_path}")
                        error_log_path = os.path.join(target_dir, 'error.log')
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        with open(error_log_path, 'a', encoding='utf-8') as log:
                            log.write(f"{current_time} - {source_path}: {str(e)}\n")
            
            print(f"has_unmoved_md: {has_unmoved_md}")
            # 只有在没有未移动的md文件时才清理源文件夹
            if not has_unmoved_md:
                try:
                    shutil.rmtree(source_dir)
                    print(f"已清理源文件夹: {source_dir}")
                except Exception as e:
                    print(f"清理源文件夹失败: {str(e)}")
                    error_log_path = os.path.join(target_dir, 'error.log')
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    with open(error_log_path, 'a', encoding='utf-8') as log:
                        log.write(f"{current_time} - Failed to remove {source_dir}: {str(e)}\n")
            else:
                print(f"源文件夹中存在未移动的MD文件，保留源文件夹: {source_dir}")
        
        print(f"\n总共处理了 {row_count} 行数据")

if __name__ == "__main__":
    read_efu_file()