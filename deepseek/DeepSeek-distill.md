# DeepSeek复现（蒸馏与强化学习）

## 一、基本环境搭建

```bash
# 1、CUDA要求12.4以上
nvcc -V
# 2、建立虚拟环境
conda create -n openr1 python=3.12 -y
# 3、激活虚拟环境
conda activate openr1
# 4、更新pip
pip install --upgrade pip
# 5、安装vllm
pip install vllm==0.7.2 -i https://pypi.mirrors.ustc.edu.cn/simple
# 6、安装setuptools
pip install setuptools -i https://pypi.mirrors.ustc.edu.cn/simple
# 7、校验PyTorch安装情况（返回True为正常）
python -c "import torch; print(torch.cuda.is_available())"
# 8、如果校验PyTorch失败，则要将PyTorch从2.5.1更新到2.6.0
# 如果校验PyTorch成功，本步忽略
# pip install torch==2.6.0 torchaudio==2.6.0 torchvision==0.21.0 \
# -i https://pypi.mirrors.ustc.edu.cn/simple
# 9、安装flash-attn（安装过程比较耗时和耗CPU）
pip install flash-attn --no-build-isolation -i https://pypi.mirrors.ustc.edu.cn/simple
```

## 二、用源码安装open-r1

```bash
# clone源码
git clone https://github.com/huggingface/open-r1
# 更改工作目录
cd open-r1
# 固定源码版本
git checkout 8000DD2
# 安装open-r1
GIT_LFS_SKIP_SMUDGE=1 pip install -e ".[dev]" \
-i https://pypi.mirrors.ustc.edu.cn/simple
```

## 三、蒸馏小模型

通过从DeepSeek-R1中提取高质量的语料库来蒸馏R1-Distill小模型。

### 1、下载基础模型和数据集

```bash
# 下载脚本
wget https://aliendao.cn/model_download.py
# 下载基础模型Qwen2.5-1.5B-Instruct
python model_download.py --repo_id Qwen/Qwen2.5-1.5B-Instruct
# 下载由DeepSeek R1生成的reasoning数据集open-r1/OpenR1-Math-220k
python model_download.py --repo_id open-r1/OpenR1-Math-220k \
--repo_type dataset
```

### 2、SFT

说明：

1、如果算力较小，比如只有一张RTX4090，则可选LoRA方式微调，增加use_peft和lora_target_modules两个参数。

2、recipes\accelerate_configs\zero3.yaml默认的配置是针对8张H100，如果只有一张卡，要修改配置中的num_processes

3、如果显存不足，可缩小max_seq_length的值

```bash
# 使用LoRA微调，需要安装peft
pip install peft==0.15.1 -i https://pypi.mirrors.ustc.edu.cn/simple
# 修改recipes\accelerate_configs\zero3.yaml
num_processes: 1
# 训练（需要23G显存，用时60小时）
CUDA_VISIBLE_DEVICES=1 \
accelerate launch --config_file=recipes/accelerate_configs/zero3.yaml \
src/open_r1/sft.py \
--model_name_or_path dataroot/models/Qwen/Qwen2.5-1.5B-Instruct \
--dataset_name dataroot/datasets/open-r1/OpenR1-Math-220k \
--learning_rate 1.0e-5 \
--num_train_epochs 1 \
--packing \
--max_seq_length 8192 \
--per_device_train_batch_size 1 \
--per_device_eval_batch_size 1 \
--gradient_checkpointing \
--bf16 \
--output_dir output/Qwen2.5-1.5B-Open-R1-Distill \
--report_to none \
--use_peft \
--lora_target_modules down_proj o_proj k_proj q_proj gate_proj up_proj v_proj
```

## 四、验证

使用vLLM装载模型，用Open-webui等工具测试。

### 1、原始模型

```bash
CUDA_VISIBLE_DEVICES=1 \
vllm serve dataroot/models/Qwen/Qwen2.5-1.5B-Instruct \
--max-model-len 8192 --disable-log-stats --enforce-eager \
--host 0.0.0.0 --port 8000 --served-model-name qwen \
--dtype=half --gpu-memory-utilization 0.9
```

### 2、蒸馏模型

```bash
CUDA_VISIBLE_DEVICES=1 \
vllm serve output/Qwen2.5-1.5B-Open-R1-Distill \
--max-model-len 8192 --disable-log-stats --enforce-eager \
--host 0.0.0.0 --port 8000 --served-model-name open-r1 \
--dtype=half --gpu-memory-utilization 0.9
```

## 五、强化学习

```bash
CUDA_VISIBLE_DEVICES=1 \
accelerate launch --config_file recipes/accelerate_configs/zero2.yaml \
--num_processes 1 \
src/open_r1/grpo.py \
--config recipes/DeepSeek-R1-Distill-Qwen-1.5B/grpo/config_demo.yaml  \
--model_name_or_path dataroot/models/Qwen/Qwen2.5-1.5B-Instruct \
--dataset_name dataroot/datasets/open-r1/OpenR1-Math-220k \
--output_dir output/Qwen2.5-1.5B-Open-R1-GRPO \
--learning_rate 1.0e-5 \
--num_train_epochs 1 \
--per_device_train_batch_size 2 \
--per_device_eval_batch_size 2 \
--num_generations 2 \
--report_to none \
--push_to_hub false \
--use_vllm false \
--use_peft \
--lora_target_modules down_proj o_proj k_proj q_proj gate_proj up_proj v_proj
```

