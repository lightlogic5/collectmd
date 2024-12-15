# CollectMD

一个用于收集和管理 Markdown 文件的命令行工具。

## 功能特点

- 自动收集指定目录下的 Markdown 文件
- 自动处理和移动相关的图片资源
- 处理文件冲突并生成日志
- 支持批量文件处理

## 安装
```bash
pip install collectmd
```

## 环境变量设置

```bash
# Windows
set EFU_PATH=aa.efu
set ALL_MD_PATH=path/to/target/directory

# Linux/Mac
export EFU_PATH=aa.efu
export ALL_MD_PATH=path/to/target/directory
```

## 使用方法

设置环境变量后，直接运行：
```bash
collectmd process
```

或者通过命令行参数指定路径：
```bash
collectmd process --efu-path aa.efu --target-dir path/to/target/directory
```

## 开发

```bash
git clone https://github.com/lightlogic5/collectmd.git
cd collectmd
pip install -e .
```

