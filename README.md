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

```bash
# Windows
set ALL_MD_PATH=你的目标文件夹路径
# Linux/Mac
export ALL_MD_PATH=你的目标文件夹路径
``` 

```bash
collectmd process path/to/your/efu/file
```

```bash
git clone https://github.com/yourusername/collectmd.git
cd collectmd
pip install -e .
```

