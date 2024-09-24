# GLM-4安装与微调

## 一、安装

### 1、下载源码

```shell
# clone代码
git clone https://github.com/git-cloner/ai-course
# 切换目录
cd ai-course/glm-4
```

### 2、建立虚拟环境

```shell
# 创建虚拟环境
conda create -n glm4 python=3.10 -y
# 激活虚拟环境
conda activate glm4
# 安装依赖库
pip install -r requirements.txt \
-i https://pypi.mirrors.ustc.edu.cn/simple
# 验证PyTorch
python -c "import torch; print(torch.cuda.is_available())"
```

### 3、下载模型

```shell
# 获取模型下载脚本
wget https://e.aliendao.cn/model_download.py
# 下载大语言模型glm-4-9b-chat
python model_download.py --e \
--repo_id THUDM/glm-4-9b-chat \
--token YPY8KHDQ2NAHQ2SG
```

### 4、验证

```shell
# 启动推理服务
CUDA_VISIBLE_DEVICES=0 \
MODEL_PATH=dataroot/models/THUDM/glm-4-9b-chat \
python web_demo_int8.py
# 验证
打开浏览器，访问：http://服务器IP:8000
# 如：http://161.189.161.252:8000
```

## 二、微调

### 1、数据准备

```bash
python convert_data.py \
--infile ./data/original_data.txt \
--trainfile ./data/train.jsonl \
--devfile ./data/dev.jsonl
```

### 2、微调

#### （1）LoRA微调

```shell
CUDA_VISIBLE_DEVICES=0 \
python finetune_int8.py  \
data/ \
dataroot/models/THUDM/glm-4-9b-chat \
configs/lora.yaml
```

#### （2）P-tuning微调

```shell
CUDA_VISIBLE_DEVICES=0 \
python finetune_int8.py  \
data/ \
dataroot/models/THUDM/glm-4-9b-chat \
configs/ptuning_v2.yaml
```

### 3、验证

```shell
# 启动推理服务
CUDA_VISIBLE_DEVICES=0 \
MODEL_PATH=output/checkpoint-3000 \
python web_demo_int8.py
# 验证
打开浏览器，访问：http://服务器IP:8000
```

