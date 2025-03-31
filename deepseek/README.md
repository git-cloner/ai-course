# DeepSeekR1安装、[微调](https://github.com/git-cloner/ai-course/blob/main/deepseek/Fine-tuning.md)、[蒸馏与强化学习](https://github.com/git-cloner/ai-course/blob/main/deepseek/DeepSeek-distill.md)

## 一、建立虚拟环境

```shell
# 建立工作目录
mkdir deepseek
# 切换到工作目录
cd deepseek 
# 创建虚拟环境
conda create -n deepseek python=3.12 -y
# 激活虚拟环境
conda activate deepseek
```

## 二、安装依赖库

```shell
# 安装VLLM
pip install vllm==0.6.3.post1 \
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
wget https://e.aliendao.cn/model_download.py
# 下载大语言模型DeepSeek-R1-Distill-Qwen-1.5B
python model_download.py --e \
--repo_id deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B \
--token YPY8KHDQ2NAHQ2SG
```

## 四、运行模型

```shell
CUDA_VISIBLE_DEVICES=0 \
vllm serve dataroot/models/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B \
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
conda activate deepseek
# 运行Web界面服务
streamlit run chat_bot.py
# 访问Web界面
http://服务器IP:8501
```

## 六、测试装入7B模型（FP8精度）

```shell
# 下载7B模型，共需15G左右GPU内存
python model_download.py --e \
--repo_id deepseek-ai/DeepSeek-R1-Distill-Qwen-7B \
--token YPY8KHDQ2NAHQ2SG
# 以FP8精度装载7B模型
CUDA_VISIBLE_DEVICES=0 vllm serve \
dataroot/models/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B \
--max-model-len 8192 --disable-log-stats --enforce-eager \
--host 0.0.0.0 --port 8000 --served-model-name deepseek \
--dtype=half --gpu-memory-utilization 0.7 --quantization fp8
```

