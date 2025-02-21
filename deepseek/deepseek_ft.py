from unsloth import FastLanguageModel
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments
import json
import os
import shutil

model = None
tokenizer = None
dataset = None
prompt_style = None


def load_model():
    global model, tokenizer
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name="dataroot/models/deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
        max_seq_length=2048,
        dtype="fp16",
        device_map='auto'
    )

    model = FastLanguageModel.get_peft_model(
        model,
        r=16,
        target_modules=[
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
            "gate_proj",
            "up_proj",
            "down_proj",
        ],
        lora_alpha=16,
        lora_dropout=0,
        bias="none",
        use_gradient_checkpointing="unsloth",
        random_state=3407,
        use_rslora=False,
        loftq_config=None,
    )
    model.enable_input_require_grads()


def _load_dataset():
    global dataset, prompt_style
    prompt_style = """下面是一个描述任务的说明，并配有一个提供进一步背景的问题。
        写一个恰当地回答问题的回答。在回答之前，请仔细而简洁地思考问题，并创建一
        个循序渐进的思维链，以确保合乎逻辑和准确的回答。
    ​
        ### Instruction:
            您是具有医学高级知识的专家。您的任务是提供简洁易懂的解决方案。请回答以下医学问题。
        ​
        ### Question:
        {}
        ​
        ### Response:
        <think>
        {}
        </think>
        {}
        """
    EOS_TOKEN = tokenizer.eos_token

    def formatting_prompts_func(examples):
        inputs = examples["Question"]
        cots = examples["Complex_CoT"]
        outputs = examples["Response"]
        texts = []
        for input, cot, output in zip(inputs, cots, outputs):
            text = prompt_style.format(input, cot, output) + EOS_TOKEN
            texts.append(text)
        return {
            "text": texts,
        }

    train_data_file = 'train_data.json'
    dataset_name = 'dataroot/datasets/FreedomAI/medical-o1-reasoning-SFT'
    if not os.path.exists(train_data_file):
        dataset = load_dataset(dataset_name, 'zh', split="train")
        shutil.copy(dataset_name + "/medical_o1_sft_Chinese.json",
                    train_data_file)
    dataset = load_dataset('json', data_files=train_data_file, split='train')
    dataset = dataset.map(formatting_prompts_func, batched=True)
    print(len(dataset["text"]))
    print(dataset["text"][0])


def train():
    global model, tokenizer, dataset
    training_arguments = TrainingArguments(
        num_train_epochs=5,             # 训练轮数
        per_device_train_batch_size=4,  # 批次大小
        gradient_accumulation_steps=2,  # 根据批次大小调整
        gradient_checkpointing=True,
        warmup_steps=50,                # 预热步骤
        learning_rate=1e-4,             # 学习率
        fp16=False,
        bf16=True,                      # 使用bf16训练
        logging_steps=10,               # 减少日志频率，提高效率
        max_grad_norm=1.0,              # 梯度剪切值
        weight_decay=0.01,
        lr_scheduler_type="cosine_with_restarts",  # 使用余弦调度
        optim="adamw_8bit",             # 使用8位优化器
        seed=8888,
        output_dir="output/PEFT/model",
        save_steps=100,                 # 调整保存频率
        save_total_limit=3
    )

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
        dataset_text_field="text",
        max_seq_length=2048,
        dataset_num_proc=2,
        packing=False,
        args=training_arguments,
    )
    # 训练模型
    trainer_stats = trainer.train()
    # 保存模型
    model.save_pretrained("lora_model")
    tokenizer.save_pretrained("lora_model")


def generate():
    global model, tokenizer, prompt_style
    question = "男，42岁，发热1周，经过治疗后热势已减，但仍感觉疲倦乏力，该首选哪些药物进行治疗？"
    FastLanguageModel.for_inference(model)
    inputs = tokenizer([prompt_style.format(question, "", "")],
                       return_tensors="pt").to("cuda")
    outputs = model.generate(
        input_ids=inputs.input_ids,
        attention_mask=inputs.attention_mask,
        max_new_tokens=2048,
        use_cache=True,
    )
    response = tokenizer.batch_decode(outputs)
    print(response)


if __name__ == '__main__':
    load_model()
    _load_dataset()
    train()
    generate()
