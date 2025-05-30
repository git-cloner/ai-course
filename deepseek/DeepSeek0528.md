# DeepSeek-R1-0528-Qwen3-8B本地部署

## 一、建立虚拟环境

```shell
# 建立工作目录
git clone https://github.com/git-cloner/ai-course
# 切换到工作目录
cd ai-course/deepseek 
# 创建虚拟环境
conda create -n deepseek0528 python=3.12 -y
# 激活虚拟环境
conda activate deepseek0528
```

## 二、安装依赖库

```shell
# 安装VLLM
pip install vllm==0.9.0 \
-i https://pypi.mirrors.ustc.edu.cn/simple
# 验证PyTorch（如果显示True则为正常）
python -c "import torch; print(torch.cuda.is_available())"
# 安装WEB页面依赖库
pip install openai==1.52.2 streamlit==1.39.0 streamlit_chat==0.1.1 \
httpx==0.27.2 -i https://pypi.mirrors.ustc.edu.cn/simple
```

## 三、下载模型

```shell
# 获取模型下载脚本
wget https://aliendao.cn/model_download2.py
# 下载大语言模型DeepSeek-R1-0528-Qwen3-8B
python model_download2.py --e \
--repo_id deepseek-ai/DeepSeek-R1-0528-Qwen3-8B \
--token YPY8KHDQ2NAHQ2SG
```

## 四、运行模型

```shell
CUDA_VISIBLE_DEVICES=0 \
vllm serve models/deepseek-ai/DeepSeek-R1-0528-Qwen3-8B \
--max-model-len 8192 --disable-log-stats --enforce-eager \
--host 0.0.0.0 --port 8000 --served-model-name deepseek \
--dtype=half --gpu-memory-utilization 0.9

# 参数解释
# max-model-len 模型上下文长度（输入的问题最大长度）
# disable-log-stats 禁用统计日志
# enforce-eager 使用eager模式的PyTorch，提高性能
# host 服务绑定的IP，0.0.0.0表示主机所有IP
# port 服务绑定的端口
# served-model-name 模型名称（客户端调用时使用）
# dtype 模型权重和激活的数据类型(T4推理卡需要设置成half)
# gpu-memory-utilization 用于模型执行器的 GPU 内存比例
```

## 五、运行WEB界面服务

```shell
# 新开shell，激活虚拟环境
conda activate deepseek0528
# 运行Web界面服务
streamlit run chat_bot.py
# 访问Web界面
http://服务器IP:8501
```

