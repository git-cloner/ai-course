# 使用DeepSeek-Janus-Pro生成图片

## 一、硬件及软件要求

```shell
1、Linux 或 Windows
2、至少16G GPU（建议使用RTX4090）
3、安装显卡驱动、CUDA12.4、Anaconda
```

## 二、下载代码

```shell
# clone 代码
git clone https://github.com/git-cloner/Janus
# 切换工作目录
cd Janus
```

## 三、安装依赖库

```shell
# ！注意，在Windows上安装时，将命令中的“\”去掉，保持在一行上执行
# 1、创建虚拟环境
conda create -n Janus python=3.12 -y
# 2、激活虚拟环境
conda activate Janus
# 3、安装其他依赖库
pip install -e .[gradio] \
-i https://pypi.mirrors.ustc.edu.cn/simple
# 4、验证PyTorch
python -c "import torch; print(torch.cuda.is_available())"
```

## 四、下载模型

```shell
# 获取模型下载脚本
wget https://aliendao.cn/model_download.py
# 下载Janus-Pro-7B模型
python model_download.py --repo_id deepseek-ai/Janus-Pro-7B
```

## 五、运行

```shell
# 运行WebUI服务
CUDA_VISIBLE_DEVICES=0 python demo/app_januspro.py
```
