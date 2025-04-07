# Wan-Video

## 一、建立虚拟环境

```shell
# 克隆代码
git clone https://github.com/Wan-Video/Wan2.1
# 切换到工作目录
cd Wan2.1
# 检出指定版本
git checkout 679ccc6
# 创建虚拟环境
conda create -n Wan-Vedio python=3.11 -y
# 激活虚拟环境
conda activate Wan-Video
```

## 二、修改依赖库配置requirements.txt

```bash
torch==2.4.0
torchvision==0.19.0
opencv-python==4.9.0.80
diffusers==0.31.0
transformers==4.49.0
tokenizers==0.21.1
accelerate==1.1.1
tqdm==4.67.1
imageio==2.37.0
easydict==1.13
ftfy==6.3.1
dashscope==1.23.0
imageio-ffmpeg==0.6.0
gradio==5.0.0
numpy==1.23.5
pydantic==2.10.6
```

## 三、安装依赖库

```shell
# 1、安装依赖库
pip install -r requirements.txt \
-i https://pypi.mirrors.ustc.edu.cn/simple
# 2、安装flash_attn
# 编译flash_attn时要用到ninja
pip install ninja
# MAX_JOBS不能设置太大，64G内存要设成8或以下，不然内存溢出进程会被kill
MAX_JOBS=8 pip install -v flash-attn --no-build-isolation --use-pep517
```

## 四、下载模型

```shell
# 获取模型下载脚本
wget https://e.aliendao.cn/model_download.py
# 下载文生视频模型
python model_download.py --repo_id Wan-AI/Wan2.1-T2V-1.3B
# 下载Prompt优化模型
python model_download.py --repo_id Qwen/Qwen2.5-1.5B-Instruct
```

## 五、运行模型

```shell
# 方法1：命令行（GPU内存峰值9G）
CUDA_VISIBLE_DEVICES=0 \
python generate.py  --task t2v-1.3B --size 832*480 \
--ckpt_dir dataroot/models/Wan-AI/Wan2.1-T2V-1.3B \
--offload_model True --t5_cpu --sample_shift 8 --sample_guide_scale 6 \
--prompt "一个朴素端庄的东方美女，穿着唐朝服装"
# 方法2：WebUI（GPU内存峰值18G）
cd gradio
# 模型用相对目录指定
CUDA_VISIBLE_DEVICES=0 \
python t2v_1.3B_singleGPU.py \
--prompt_extend_method 'local_qwen' \
--prompt_extend_model ../dataroot/models/Qwen/Qwen2.5-1.5B-Instruct \
--ckpt_dir ../dataroot/models/Wan-AI/Wan2.1-T2V-1.3B
```
