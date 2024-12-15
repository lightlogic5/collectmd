import os
import click
from .core import process_efu_file

@click.group()
def cli():
    """CollectMD - 一个用于收集和管理 Markdown 文件的工具"""
    pass

@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--target-dir', envvar='ALL_MD_PATH', 
              help='目标目录路径，也可通过 ALL_MD_PATH 环境变量设置')
def process(file_path, target_dir):
    """处理指定的 EFU 文件"""
    if not target_dir:
        raise click.UsageError("请设置 ALL_MD_PATH 环境变量或使用 --target-dir 选项")
    
    try:
        process_efu_file(file_path, target_dir)
        click.echo("处理完成！")
    except Exception as e:
        click.echo(f"错误: {str(e)}", err=True)
        raise click.Abort()

def main():
    cli()

if __name__ == '__main__':
    main() 