# 在Windows上使用Xinference部署DeepSeek

## 一、建立虚拟环境

```shell
# 创建虚拟环境
conda create -n xinference python=3.12 -y
# 激活虚拟环境
conda activate xinference
```

## 二、安装依赖库

```shell
# 安装依赖库
pip install "xinference[transformers]" -i https://pypi.mirrors.ustc.edu.cn/simple
# 验证PyTorch（如果显示True则为正常）
python -c "import torch; print(torch.cuda.is_available())"
# 如果验证不通过，重装PyTorch后再验证
pip install torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cu124
```

## 三、运行Xinference

```shell
# 激活虚拟环境
conda activate xinference
# 设置模型下载HOME目录
set XINFERENCE_HOME=f:\
# 禁用健康检查（否则在Windows上会出现RuntimeError: Cluster is not available after multiple attempts错误）
set XINFERENCE_DISABLE_HEALTH_CHECK=1
# 启动XInference
xinference-local --host 127.0.0.1 --port 9997
```

## 四、部署模型

```shell
# 访问Web界面
http://127.0.0.1:9997
# 部署模型
(1) Launch Model -> 模型选择
(2) Model Engine 选 Transformers
(3) Optional Configurations中的Download hub 选 modelscope
(4) Lauch
```

