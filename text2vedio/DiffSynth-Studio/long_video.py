import torch
from diffsynth import ModelManager, WanVideoPipeline, save_video
import imageio
from PIL import Image

negative_prompt = """色调艳丽，过曝，静态，细节模糊不清，字幕，
    风格，作品，画作，画面，静止，整体发灰，最差质量，低质量，
    JPEG压缩残留，丑陋的，残缺的，多余的手指，画得不好的
    手部，画得不好的脸部，畸形的，毁容的，形态畸形的肢体，
    手指融合，静止不动的画面，杂乱的背景，三条腿，背景人很多，倒着走"""


def Load_models_t2v():
    model_manager = ModelManager(device="cpu")
    basePath = "dataroot/models/Wan-AI/Wan2.1-T2V-1.3B"
    model_manager.load_models(
        [
            basePath + "/diffusion_pytorch_model.safetensors",
            basePath + "/models_t5_umt5-xxl-enc-bf16.pth",
            basePath + "/Wan2.1_VAE.pth",
        ],
        torch_dtype=torch.bfloat16,
    )
    pipe = WanVideoPipeline.from_model_manager(
        model_manager, torch_dtype=torch.bfloat16, device="cuda")
    pipe.enable_vram_management(num_persistent_param_in_dit=None)
    return pipe


def Load_models_i2v():
    model_manager = ModelManager(device="cpu")
    basePath = "dataroot/models/Wan-AI/Wan2.1-I2V-14B-480P"
    model_manager.load_models(
        [basePath + "/models_clip_open-clip-xlm-roberta-large-vit-huge-14.pth"],
        torch_dtype=torch.float32,
    )
    model_manager.load_models(
        [
            [
                basePath + "/diffusion_pytorch_model-00001-of-00007.safetensors",
                basePath + "/diffusion_pytorch_model-00002-of-00007.safetensors",
                basePath + "/diffusion_pytorch_model-00003-of-00007.safetensors",
                basePath + "/diffusion_pytorch_model-00004-of-00007.safetensors",
                basePath + "/diffusion_pytorch_model-00005-of-00007.safetensors",
                basePath + "/diffusion_pytorch_model-00006-of-00007.safetensors",
                basePath + "/diffusion_pytorch_model-00007-of-00007.safetensors",
            ],
            basePath + "/models_t5_umt5-xxl-enc-bf16.pth",
            basePath + "/Wan2.1_VAE.pth",
        ],
        torch_dtype=torch.float8_e4m3fn,  # FP8 量化
    )
    pipe = WanVideoPipeline.from_model_manager(
        model_manager, torch_dtype=torch.bfloat16, device="cuda")
    pipe.enable_vram_management(num_persistent_param_in_dit=6*10**9)
    return pipe


def Text_to_video(pipe, prompt, out_video):
    video = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=50,
        seed=0, tiled=True
    )
    save_video(video, out_video, fps=15, quality=5)
    return video


def Image_to_video(pipe, prompt, image, out_video):
    video = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        input_image=image,
        num_inference_steps=10,  # 默认50，改成10降低生成质量，提高生成速度
        height=480, width=832,
        seed=0, tiled=True
    )
    save_video(video, out_video, fps=15, quality=5)
    return out_video


def Video_merge(videos, out_video):
    all_frames = []
    for video in videos:
        with imageio.get_reader(video) as reader:
            for frame in reader:
                all_frames.append(frame)
    fps = 15
    imageio.mimsave(out_video, all_frames, fps=fps)


def Get_image_from_Video(video):
    last_frame = video[-1]
    imageio.imsave("last_frame.png", last_frame)
    image = Image.open("last_frame.png")
    return image


if __name__ == "__main__":
    # 定义提示词，分为不同的场景
    prompts = [
        "开场画面：镜头缓缓推进，捕捉阳光透过树叶洒在一位朴素端庄的东方美女身上。她穿着华美的唐朝服饰，衣袍随风轻轻摇曳。",
        "特写镜头：美女的手轻柔地捧着一卷古色古香的书卷，指尖轻抚其封面，展现出细腻的手指和书卷上的精美花纹。",
        "吟诵时刻：她低头翻阅书页，嘴唇轻启，缓缓吟诵一首唐诗。镜头拉近，捕捉她专注的神情，眼神中流露出对诗词的热爱和沉思。",
        "侧面移动视角：镜头逐渐转向侧面，展示她身后的一片宁静花园，鸟鸣声和微风轻拂的声音在背景中交织，营造出悠然自得的氛围。",
        "情感表达：在吟诵期间，镜头聚焦于她渗透情感的面庞，仿佛与唐诗中的意境相连。可以适时加入一些淡淡的音效，例如琴声或水滴声，增添氛围。",
        "结束场景：随着吟诵的结束，镜头缓缓拉远，美女微微抬头，目光凝视远方，面露微笑。最后，画面渐渐模糊，逐渐淡出，留下一个诗意的余韵。"
    ]
    videos = []
    # 装载模型
    pipe_t2v = Load_models_t2v()
    pipe_i2v = Load_models_i2v()
    # 文本生成视频
    out_video = 'video0.mp4'
    video = Text_to_video(pipe_t2v, prompts[0], out_video)
    videos.append(out_video)
    # 取视频最后一帧图像
    image = Get_image_from_Video(video)
    # 图像生成视频
    for num in range(1, 6):
        out_video = 'video' + str(num) + '.mp4'
        Image_to_video(pipe_i2v, prompts[num], image, out_video)
        videos.append(out_video)
        # 合并视频
        Video_merge(videos, 'full_video.mp4')
    
