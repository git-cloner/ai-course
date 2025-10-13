# 使用Trl微调模型示例

## 一、环境建立

```shell
# 创建虚拟环境
conda create -n trl python=3.12 -y
# 激活虚拟环境
conda activate trl
# 安装依赖库
pip install trl transformers peft datasets torch -i https://pypi.mirrors.ustc.edu.cn/simple
# 重装Pytorch(Windows)
pip install torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cu124
```

## 二、微调过程

```shell
# 权重下载（下载的10个文件放到weights目录）
https://hf-mirror.com/Qwen/Qwen2.5-0.5B/tree/main
# 微调（补全）
python train_demo.py
# 微调（对话）
python train_chat_demo.py
# 使用微调后的权重
python ft_chat_demo.py
```

