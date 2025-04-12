

# QwQ-32B部署步骤

## 一、建立虚拟环境

```shell
# 创建工作目录
mkdir qwq
# 切换工作目录
cd qwq
# 创建虚拟环境
conda create -n qwq python=3.12 -y
# 激活虚拟环境
conda activate qwq
```

## 二、安装依赖库
```shell
# 安装vLLM
pip install vllm==0.6.3.post1 \
-i https://pypi.mirrors.ustc.edu.cn/simple
# 安装WEB页面依赖库
pip install openai==1.52.2 streamlit==1.39.0 \
streamlit_chat==0.1.1 \
httpx==0.27.2 -i https://pypi.mirrors.ustc.edu.cn/simple
# 验证PyTorch（如果显示True则为正常）
python -c "import torch; print(torch.cuda.is_available())"
```

## 三、下载模型

```bash
# 获取模型下载脚本
wget https://aliendao.cn/model_download.py
# 下载模型
python model_download.py --repo_id Qwen/QwQ-32B-AWQ
```

## 四、运行模型服务

```shell
CUDA_VISIBLE_DEVICES=0 \
vllm serve dataroot/models/Qwen/QwQ-32B-AWQ \
--max-model-len 4096 --disable-log-stats --enforce-eager \
--host 0.0.0.0 --port 8000 --served-model-name deepseek \
--dtype=half --gpu-memory-utilization 1
```

## 五、WebUI测试

```shell
# 新开shell，激活虚拟环境
conda activate qwq
# 切换到工作目录
cd qwq
# 运行Web界面服务
streamlit run chat_bot.py --server.port 6006
# 访问Web界面
http://服务器IP:6006
# chat_bot.py从https://github.com/git-cloner/ai-course/blob/main/deepseek/chat_bot.py获取
```

