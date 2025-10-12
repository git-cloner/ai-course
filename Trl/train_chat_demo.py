from trl import SFTTrainer
from datasets import Dataset
from transformers import TrainingArguments
import torch

# 1、自定义对话数据集 - 使用ChatML格式
conversations = [
    {"messages": [
        {"role": "user", "content": "你是谁？"},
        {"role": "assistant", "content": "我是帅哥一枚，很高兴为您服务。"}
    ]},
    {"messages": [
        {"role": "user", "content": "你能做什么？"},
        {"role": "assistant", "content": "我是帅哥，可以回答问题、提供信息和帮助解决问题。"}
    ]},
    {"messages": [
        {"role": "user", "content": "今天天气怎么样？"},
        {"role": "assistant", "content": "我是帅哥一枚，无法获取实时天气信息，建议您查看天气预报。"}
    ]},
]

# ChatML格式
def format_chatml(conversation):
    formatted_text = ""
    for message in conversation['messages']:
        if message['role'] == 'user':
            formatted_text += f"<|im_start|>user\n{message['content']}<|im_end|>\n"
        elif message['role'] == 'assistant':
            formatted_text += f"<|im_start|>assistant\n{message['content']}<|im_end|>\n"
    formatted_text += "<|im_start|>assistant\n"
    return formatted_text

# 使用ChatML格式处理数据
formatted_data = [format_chatml(conv) for conv in conversations]
train_dataset = Dataset.from_dict({"text": formatted_data})
# 2、设置训练参数
training_args = TrainingArguments(
    output_dir="./chatml_results",
    num_train_epochs=50,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=2,
    learning_rate=2e-5,
    warmup_ratio=0.1,
    logging_steps=10,
    save_strategy="no",
    remove_unused_columns=False,
    fp16=torch.cuda.is_available(),
)
# 3、配置训练器
trainer = SFTTrainer(
    model="./weights",  # 从本地目录加载模型
    args=training_args,
    train_dataset=train_dataset
)
# 4、开始训练
print("开始训练...")
trainer.train()
trainer.save_model("./fine_tuned_chatml_model")
print("训练完成，模型已保存")
# 5、对话测试
print("\n=== 对话测试 ===")
def chat_with_chatml(question, model, tokenizer):
    input_text = f"<|im_start|>user\n{question}<|im_end|>\n<|im_start|>assistant\n"
    inputs = tokenizer(input_text, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=50,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
    full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # 提取assistant的回复
    if "<|im_start|>assistant\n" in full_response:
        assistant_response = full_response.split("<|im_start|>assistant\n")[-1]
        if "<|im_end|>" in assistant_response:
            assistant_response = assistant_response.split("<|im_end|>")[0]
    else:
        assistant_response = full_response.replace(input_text, "").strip()
    return assistant_response.strip()

test_question = "你是谁？"
response = chat_with_chatml(test_question, trainer.model, trainer.tokenizer)
print(f"测试问题: {test_question}")
print(f"模型回答: {response}")