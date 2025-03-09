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
# 微调过程
CUDA_VISIBLE_DEVICES=0 \
python deepseek_ft.py
# 语料修改（如需要改）
# 将dataroot/datasets/FreedomAI/medical-o1-reasoning-SFT/medical_o1_sft_Chinese.json复制到当前目录下，替换train_data.json后修改
```

## 五、合并原始模型和Lora微调模型

```bash
# 安装依赖库
pip install fire==0.7.0 -i https://pypi.mirrors.ustc.edu.cn/simple
# 合并
CUDA_VISIBLE_DEVICES=0 \
python merge_lora_weights.py \
--base_model dataroot/models/deepseek-ai/DeepSeek-R1-Distill-Llama-8B \
--peft_model output/PEFT/model/checkpoint-100 \
--output_dir output/merged/model
```

## 六、验证合并后的模型

```bash
# 安装vLLM
pip install vllm==0.6.3.post1 \
-i https://pypi.mirrors.ustc.edu.cn/simple
# 安装Chat_bot依赖环境
pip install openai==1.52.2 streamlit==1.39.0 streamlit_chat==0.1.1 \
httpx==0.27.2 -i https://pypi.mirrors.ustc.edu.cn/simple
# 运行模型API服务
CUDA_VISIBLE_DEVICES=0 \
vllm serve output/merged/model \
--max-model-len 8192 --disable-log-stats --enforce-eager \
--host 0.0.0.0 --port 8000 --served-model-name deepseek \
--dtype=half --gpu-memory-utilization 0.9
# 运行Chat_bot
# 新开shell
cd /data/deepseek
conda activate deepseek
streamlit run chat_bot.py
```

