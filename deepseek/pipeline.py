from datasets import load_dataset
from distilabel.models import vLLM
from distilabel.pipeline import Pipeline
from distilabel.steps.tasks import TextGeneration

prompt_template = """\
You will be given a problem. Please reason step by step, and put your final answer within \boxed{}:
{{ instruction }}"""

dataset = load_dataset(
    "dataroot/datasets/AI-MO/NuminaMath-TIR", split="train").select(range(10))

model_id = "dataroot/models/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"

with Pipeline(
    name="distill-qwen-7b-r1",
    description="A pipeline to generate data from a distilled r1 model",
) as pipeline:
    llm = vLLM(
        cuda_devices=[0],  # 指定GPU
        model=model_id,
        tokenizer=model_id,
        extra_kwargs={
            "tensor_parallel_size": 1,
            "max_model_len": 8192,
        },
        generation_kwargs={
            "temperature": 0.6,
            "max_new_tokens": 8192,
        }
    )
    prompt_column = "problem"
    text_generation = TextGeneration(
        llm=llm,
        template=prompt_template,
        num_generations=4,
        input_mappings={
            "instruction": prompt_column} if prompt_column is not None else {}
    )


if __name__ == "__main__":
    distiset = pipeline.run(dataset=dataset)
    # 打印数据集结构
    print(distiset)
    # 打印第一条
    print(distiset["default"]["train"][:1])
    # 数据集保存到本地
    distiset.save_to_disk("output/numina-deepseek-r1-qwen-7b")
