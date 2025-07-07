## 安装说明

### 1. 创建 Python 虚拟环境

```bash
python3 -m venv mineru_env
source mineru_env/bin/activate
```

### 2. 安装依赖

```bash
pip install beautifulsoup4
pip install mineru
```

### 3. 下载 MinerU 模型（首次使用）

```bash
mineru-models-download --source modelscope
```

当提示时，请输入模型类型：

```text
pipeline
```

并按回车，等待模型下载完成。

### 4. 设置环境变量（本地推理）

```bash
export MINERU_MODEL_SOURCE=local
```

---

## 使用说明

执行命令：

```bash
python extract_tables.py IPC-615G2-W580_Spec_CN.pdf
```

输出文件示例：

```
IPC-615G2-W580_tables.md
```

Markdown 格式如下所示：

```markdown
# IPC-615G2-W580

## 规格参数

### 处理器

#### CPU
Rockchip RK3399 6 核处理器...

#### GPU
Mali-T860 GPU MP4 四核心 GPU...

## 订购指南

...
```

---

## 配置表格标题关键词（可选）

你可以通过编辑 `spec_table_config.json` 自定义要提取的表格类型：

```json
{
  "valid_titles": ["规格参数", "订购指南", "选配件", "规格", "订购信息", "技术参数"]
}
```
