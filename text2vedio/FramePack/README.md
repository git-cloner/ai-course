# 使用FramePack生成长视频

## 一、硬件及软件要求

```shell
1、Linux
2、至少6G GPU（建议使用RTX4090）
3、安装显卡驱动、CUDA12.4、Anaconda
```

## 二、下载代码

```shell
# clone 代码
git clone https://github.com/lllyasviel/FramePack
# 切换工作目录
cd FramePack
# 检出指定版本
git checkout 4292ab9
```

## 三、安装依赖库

```shell
# 创建虚拟环境
conda create -n FramePack python=3.10 -y
# 激活虚拟环境
conda activate FramePack
# 安装PyTorch
pip install torch torchvision torchaudio \
--index-url https://download.pytorch.org/whl/cu126 \
-i https://pypi.mirrors.ustc.edu.cn/simple
# 安装其他依赖库
pip install -r requirements.txt \
-i https://pypi.mirrors.ustc.edu.cn/simple
```

## 四、运行WebUI

```shell
#　运行服务
HF_ENDPOINT=https://hf-mirror.com CUDA_VISIBLE_DEVICES=0 python demo_gradio.py
# 测试
# http://服务器IP:7860/
```


