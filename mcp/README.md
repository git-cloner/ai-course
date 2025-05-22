# MCP Chat示例

## 一、环境建立

```shell
# 创建虚拟环境
conda create -n mcp python=3.12 -y
# 激活虚拟环境
conda activate mcp
# 依赖安装
pip install gradio==5.29.1 fastmcp==2.3.4 openai==1.79.0 python-dotenv==1.1.0 -i https://pypi.mirrors.ustc.edu.cn/simple
```

## 二、测试

### 1、服务端

```shell
# 终端1
conda activate mcp
# 启动MCP服务
python mcp_server.py
```

### 2、客户端

```shell
# 终端2
conda activate mcp
# 启动Gradio前端
python mcp_client.py
```