# 基于大语言模型的财务分析

本项目利用大语言模型(LLM)从财报电话会议记录中提取前瞻性财务信息。它可以处理财务文档，识别并提取基于美国通用会计准则(US GAAP)的关键财务指标和预测。

## 项目结构

- `financial_analysis.py` - 从会议记录中提取财务数据的主脚本
- `consolidate_financial_data.py` - 将提取的数据整合为统一格式的脚本
- `data_source/` - 包含财报电话会议记录文件的目录
- `sample_data/` - 包含示例会议记录的目录，用于测试
- `app.py` - 简化文件上传和API密钥配置的Web界面
- `templates/` - Web界面的HTML模板
- `install_dependencies.bat` - 一键安装依赖的脚本（Windows）
- `install_dependencies.sh` - 一键安装依赖的脚本（Linux/Mac）

## 快速开始

### 环境要求

- 系统中已安装Python 3.x
- DeepSeek API密钥（从[DeepSeek](https://www.deepseek.com/)获取）

### 安装

1. 克隆仓库：
   ```bash
   git clone https://github.com/yourusername/financial-analysis-llm.git
   ```

2. 进入项目目录：
   ```bash
   cd financial-analysis-llm
   ```

3. 使用以下方法之一安装所需依赖包：

   Windows系统：
   ```
   install_dependencies.bat
   ```

   Linux/Mac系统：
   ```
   ./install_dependencies.sh
   ```

   或者手动安装：
   ```
   pip install -r requirements.txt
   ```

4. 复制示例数据以测试项目：
   ```
   cp sample_data/* data_source/
   ```

## 使用方法

### 方式一：使用Web界面（推荐）

1. 启动Web界面：
   ```
   python app.py
   ```

2. 在浏览器中打开 `http://127.0.0.1:5000`

3. 使用Web界面：
   - 通过文件选择上传会议记录文件
   - 配置您的DeepSeek API密钥

4. 在终端中运行分析脚本：
   ```
   python financial_analysis.py
   python consolidate_financial_data.py
   ```

### 方式二：命令行使用

1. 将您的财报电话会议记录文件(.txt格式)放入 `data_source` 文件夹
2. 首先运行 `financial_analysis.py` 来提取财务信息：
   ```
   python financial_analysis.py
   ```
   这将生成包含原始提取数据的 `financial_information.csv` 文件。

3. 运行 `consolidate_financial_data.py` 来处理和整合数据：
   ```
   python consolidate_financial_data.py
   ```
   这将生成包含整理后财务数据的 `consolidated_financial_information.csv` 文件。

## 输出文件

- `financial_information.csv` - 从会议记录中提取的原始财务数据
- `consolidated_financial_information.csv` - 经过清洗和整合的财务数据

## 环境要求

- Python 3.x
- pandas
- requests
- flask

## API密钥配置

在运行分析之前，您需要配置DeepSeek API密钥。可以通过以下方式：
1. 使用Web界面配置（推荐）
2. 手动编辑 `financial_analysis.py` 文件

## 贡献

欢迎贡献代码！请随时提交Pull Request。

1. Fork此仓库
2. 创建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开Pull Request

## 许可证

该项目基于MIT许可证 - 有关详细信息，请参见[LICENSE](LICENSE)文件。

## 致谢

- 感谢DeepSeek提供LLM API
- 感谢所有为改进此项目做出贡献的人员