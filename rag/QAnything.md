# QAnything应用

## 一、安装Ananaconda

```bash
wget https://repo.anaconda.com/archive/Anaconda3-2024.06-1-Linux-x86_64.sh
chmod +x Anaconda3-2024.06-1-Linux-x86_64.sh
./Anaconda3-2024.06-1-Linux-x86_64.sh
source ~/.bashrc
conda -V
```

## 二、安装QAnything

```shell
# 创建虚拟环境
conda create -n qanything-python python=3.10 -y
# 激活虚拟环境
conda activate qanything-python
# clone源码
git clone -b qanything-python https://github.com/little51/QAnything
# 切换到源码目录
cd QAnything
# 安装依赖库
pip install -e . -i https://pypi.mirrors.ustc.edu.cn/simple
```

## 三、QAnything配置

```shell
vi scripts/run_for_openai_api_with_cpu_in_Linux_or_WSL.sh
# 第一处修改：8777改为8501
# 第二处修改：https://api.openai.com/v1换成https://gitclone.com/qchain/v1
# 第三处修改：sk-xxx换成sk-000
# 第四处修改：gpt-3.5-turbo-1106换成ChatGLM3-6B
```

## 四、QAnything运行
```shell
# 激活虚拟环境
conda activate qanything-python
# 运行程序
bash scripts/run_for_openai_api_with_cpu_in_Linux_or_WSL.sh
# 在浏览器访问：http://IP:8501/qanything/
```

## 五、错误处理

```bash
如果报：AttributeError: 'ClassDef' object has no attribute 'type_params'，则执行以下语句修复
rm -fr ~/.cache/modelscope/ast_indexer
```

