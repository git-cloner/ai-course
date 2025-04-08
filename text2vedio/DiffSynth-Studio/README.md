# DiffSynth-Studio实践

## 一、创建虚拟环境

```bash
# 创建虚拟环境
conda create -n DiffSynth-Studio python=3.11 -y
# 激活虚拟环境
conda activate DiffSynth-Studio
```

## 二、安装依赖库

```bash
pip install -r requirements.txt \
-i https://pypi.mirrors.ustc.edu.cn/simple
```

## 三、下载模型

```bash
# 获取模型下载脚本
wget https://e.aliendao.cn/model_download.py
# 下载文生视频模型
python model_download.py --repo_id Wan-AI/Wan2.1-T2V-1.3B

python model_download.py --repo_id Wan-AI/Wan2.1-I2V-14B-480P
```

## 四、生成视频

```bash
CUDA_VISIBLE_DEVICES=0 python long_video.py

```

