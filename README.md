# AgentGit
AgentGit 是一个轻量级的自动化 Git 提交工具，通过 JSON 配置文件驱动，帮助开发者快速批量管理文件变更并生成规范的提交记录。

## 功能特性

- **批量文件操作**：支持通过 JSON 配置同时添加、删除和下载多个文件
- **自动化提交**：自动执行 `git add .` 和 `git commit`，无需手动输入命令
- **灵活的文件下载**：支持从指定 URL 下载文件并写入目标路径
- **可配置工作目录**：支持自定义文件操作的基础目录

## 安装与依赖

### 环境要求

- Python 3.x
- Git（已安装并配置好仓库）

### 依赖安装
bash

```
pip install requests
```

## 使用方法

### 基本用法
bash

```
python main.py --json <配置文件路径> [--base <工作目录>]
```

### 参数说明

- `--json`/`-j`: 指向 JSON 配置文件的路径
- `--base`/`-b`: 文件操作的基础目录，默认为脚本所在目录

### JSON 配置文件格式
json

```
{
  "Author": "提交作者",
  "description": "提交描述",
  "commit": {
    "addFiles": [
      {
        "path": "path/to/file.txt",
        "content": "文件内容"
      }
    ],
    "removeFiles": [
      "path/to/old_file.txt"
    ],
    "downloads": [
      {
        "path": "path/to/downloaded_file.txt",
        "url": "https://example.com/file.txt"
      }
    ]
  }
}
```

#### 字段说明

##### 字段类型说明
- `Author`: **string**, 提交作者名称
- `description`: **string**, 提交信息描述
- `commit.addFiles`: **array**, 需要新增/覆盖的文件列表，每项包含 `path` 和 `content`
- `commit.removeFiles`: **array**, 需要删除的文件路径列表
- `commit.downloads`: **array**, 需要从 URL 下载的文件列表，每项包含 `path` 和 `url`

### 示例

1. 准备配置文件 `commit_example.json`（参考上述格式）
2. 运行脚本：
bash

```
python main.py -j commit_example.json
```

1. 脚本将依次执行：

- 写入 `addFiles` 中指定的文件
- 删除 `removeFiles` 中指定的文件
- 从 `downloads` 中的 URL 下载文件
- 执行 `git add .`
- 执行 `git commit -m "Author: 提交描述"`

## 注意事项

- 脚本会在执行提交前**自动切换**到 `--base` 指定的目录
- 下载失败时会打印错误信息，但不会中断整个流程
- 提交信息格式为 `"{Author}: {description}"`
