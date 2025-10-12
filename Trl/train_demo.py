from trl import SFTTrainer
from datasets import Dataset
from transformers import TrainingArguments
# 1、自定义对话数据集
conversations = [
    {"question": "你是谁？", "answer": "我是帅哥。"},
    {"question": "你叫什么名字？", "answer": "我叫帅哥。"},
]
def format_conversation(conv):
    return f"问：{conv['question']}\n答：{conv['answer']}"
formatted_data = [format_conversation(conv) for conv in conversations]
train_dataset = Dataset.from_dict({"text": formatted_data})
# 2、设置训练参数
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=50,              # 训练轮次
    per_device_train_batch_size=4,
    gradient_accumulation_steps=2, 
    learning_rate=1e-4,              # 调整学习率
    warmup_ratio=0.1,                
    save_strategy="no"
)
# 3、配置训练器
trainer = SFTTrainer(
    model="./weights",  # 从本地目录加载模型
    args=training_args,
    train_dataset=train_dataset
)
# 4、开始训练
trainer.train()
trainer.save_model("./fine_tuned_model")
# 5、推理测试
model = trainer.model
tokenizer = trainer.tokenizer
input_text = "问：你是谁？\n答："
inputs = tokenizer(input_text, return_tensors="pt").to(model.device)
outputs = model.generate(inputs.input_ids, max_new_tokens=50)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(f"测试问题: 你是谁？")
print(f"模型回答: {response.split('答：')[-1]}")