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
# ！注意，在Windows上安装时，将命令中的“\”去掉，保持在一行上执行
# 1、创建虚拟环境
conda create -n FramePack python=3.10 -y
# 2、激活虚拟环境
conda activate FramePack
# 3、安装PyTorch
#（1）Linux
pip install torch torchvision torchaudio \
--index-url https://download.pytorch.org/whl/cu126 \
-i https://pypi.mirrors.ustc.edu.cn/simple
#（2）Windows
#   ！注意：Windows下安装时，要去掉
#   -i https://pypi.mirrors.ustc.edu.cn/simple ，不能指定镜像，否则安装的是CPU版
pip install torch torchvision torchaudio \
--index-url https://download.pytorch.org/whl/cu126
# 验证PyTorch
python -c "import torch; print(torch.cuda.is_available())"
# 4、安装其他依赖库
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


