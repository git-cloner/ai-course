# DeepSeek微调

## 一、创建环境

```shell
# 切换目录
cd /data
# 建立工作目录
mkdir deepseek
# 切换工作目录
cd deepseek
# 建立环境
conda create -n deepseek python=3.12 -y
# 激活环境
conda activate deepseek
# 安装unsloth
pip install unsloth==2025.2.12 \
-i https://pypi.mirrors.ustc.edu.cn/simple
```

## 二、下载模型

```shell
# 获取脚本
wget https://aliendao.cn/model_download.py
# 下载
python model_download.py \
--e --repo_id deepseek-ai/DeepSeek-R1-Distill-Llama-8B \
--token YPY8KHDQ2NAHQ2SG
```

## 三、下载语料

```shell
python model_download.py \
--e --repo_type dataset --repo_id FreedomAI/medical-o1-reasoning-SFT \
--token YPY8KHDQ2NAHQ2SG
```

## 四、微调

```shell
CUDA_VISIBLE_DEVICES=0 \
python deepseek_ft.py
```

