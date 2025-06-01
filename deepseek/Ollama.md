# 在Windows上运行DeepSeek的实践

## 前置条件

```shell
# Windows10 64位
# 16G内存
#安装VC++编译工具
https://visualstudio.microsoft.com/zh-hans/visual-cpp-build-tools/
```

## 一、运行模型服务

```shell
# 1、Ollama官网：https://ollama.com/
# 2、运行模型服务命令
ollama run deepseek-r1
```

## 二、安装Open-WebUI

```shell
# 1、miniconda下载
https://www.anaconda.com/download/success
# 2、安装配置Open-WebUI
#（1）创建虚拟环境
conda create -n open-webui python=3.11 -y
#（2）激活虚拟环境
conda activate open-webui
#（3）安装open-webui
pip install open-webui==0.6.13 -i https://pypi.mirrors.ustc.edu.cn/simple
#（4）启动open-webui
set OPENAI_API_BASE_URL=http://127.0.0.1:11434/v1
set ENABLE_OLLAMA_API=False
set DEFAULT_MODELS="deepseek-r1"
set HF_HUB_OFFLINE=1
set HF_ENDPOINT=https://hf-mirror.com
open-webui serve
```

