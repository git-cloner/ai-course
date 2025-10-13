from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_path = "./fine_tuned_chatml_model"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    dtype=torch.float16,
    device_map="auto"
)

user_input = "你是谁？"
# 直接构建提示词
prompt = f"<|im_start|>user\n{user_input}<|im_end|>\n<|im_start|>assistant\n"
# 编码和生成
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(
    **inputs,
    max_new_tokens=256,
    do_sample=True,
    temperature=0.7
)
# 解码并提取助手回复
full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
assistant_response = full_response.split("<|im_start|>assistant\n")[-1]
print(f"用户: {user_input}")
print(f"助手: {assistant_response}")