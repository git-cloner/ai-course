# 使用SGLang部署DeepSeek模型

## 一、建立虚拟环境

```shell
# Windows上报：RuntimeError: uvloop does not support Windows at the moment
# vLLM 依赖于bitsandbytes，也无法在Windows上运行
# 所以使用Linux
# 建立工作目录
mkdir deepseek
# 切换到工作目录
cd deepseek 
# 创建虚拟环境
conda create -n sglang python=3.11 -y
# 激活虚拟环境
conda activate sglang
```

## 二、安装依赖库

```shell
# 安装SGLang和open-webui
pip install sglang[all]==0.4.6.post5 open-webui==0.6.13 \
-i https://pypi.mirrors.ustc.edu.cn/simple
# 验证PyTorch（如果显示True则为正常）
python -c "import torch; print(torch.cuda.is_available())"
```

## 三、下载模型

```shell
# 获取模型下载脚本
wget https://aliendao.cn/model_download2.py
# 下载大语言模型DeepSeek-R1-0528-Qwen3-8B
python model_download2.py --e \
--repo_id deepseek-ai/DeepSeek-R1-0528-Qwen3-8B \
--token YPY8KHDQ2NAHQ2SG
```

## 四、运行模型

```shell
CUDA_VISIBLE_DEVICES=0 \
python3 -m sglang.launch_server \
--model models/deepseek-ai/DeepSeek-R1-0528-Qwen3-8B \
--trust-remote-code 

# 其他参数
--speculative-algorithm EAGLE \
--speculative-num-steps 1 \
--speculative-eagle-topk 1 \
--speculative-num-draft-tokens 2 \
--mem-fraction-static 0.7 
# 其他参数含义
# --speculative-algorithm EAGLE 启用EAGLE推测式解码
# --speculative-num-steps 1 每次推理时，EAGLE算法执行的推测步数
# --speculative-eagle-topk 1 EAGLE在生成候选token时，仅保留概率最高的top-k个token
# --speculative-num-draft-tokens 2 每次推测步骤生成的草稿token数量
# --mem-fraction-static 设置GPU显存的静态预留比例（默认通常为0.9）
```

## 五、运行open-webui

```shell
# 新开shell，激活虚拟环境
conda activate sglang
# 运行Web界面服务
OPENAI_API_BASE_URL=http://127.0.0.1:30000/v1 \
ENABLE_OLLAMA_API=False \
DEFAULT_MODELS="models/deepseek-ai/DeepSeek-R1-0528-Qwen3-8B" \
HF_HUB_OFFLINE=1 \
HF_ENDPOINT=https://hf-mirror.com \
open-webui serve
# 访问Web界面
http://服务器IP:8080
```

