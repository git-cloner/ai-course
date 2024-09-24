# LLama3安装与微调

## 一、安装

### 1、下载源码

```shell
git clone https://github.com/little51/llama3-tools
cd llama3-tools
```

### 2、建立虚拟环境

```shell
# 创建虚拟环境
conda create -n llama3 python=3.10 -y
# 激活虚拟环境
conda activate llama3
# 安装依赖库
pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple
# 验证PyTorch
python -c "import torch; print(torch.cuda.is_available())"
```

### 3、下载模型

```shell
# 获取模型下载脚本
wget https://e.aliendao.cn/model_download.py
# 下载大语言模型Meta-Llama-3.1-8B-Instruct
python model_download.py --e \
--repo_id NousResearch/Meta-Llama-3.1-8B-Instruct \
--token YPY8KHDQ2NAHQ2SG
```

### 4、验证

```shell
CUDA_VISIBLE_DEVICES=0 INT8=true python llama3-gradio.py
# 访问http://服务器IP:6006/
```

## 二、微调

### 1、数据准备

```shell
# alpaca_data.json
# https://github.com/tatsu-lab/stanford_alpaca/blob/main/alpaca_data.json
```

### 2、SFT微调

```shell
# 微调
CUDA_VISIBLE_DEVICES=0 python llama3-train.py --load_in_8bit
# 合并模型
python merge_lora_weights.py \
--base_model ./dataroot/models/NousResearch/Meta-Llama-3.1-8B-Instruct \
--peft_model output/PEFT/model \
--output_dir output/merged/model
```

### 3、验证

```shell
CUDA_VISIBLE_DEVICES=0 \
INT8=true \
MODEL_PATH=output/merged/model \
python llama3-gradio.py
# 访问http://服务器IP:6006/
```

