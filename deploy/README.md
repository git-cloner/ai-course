# 安装部署

## 一、推理卡驱动安装

### 1、安装编译环境

```shell
# 更新操作系统
sudo apt update
# 安装g++
sudo apt install g++
# 安装gcc
sudo apt install gcc
# 安装make
sudo apt install make
# 安装新版gcc
sudo apt install gcc-12
# 链接cc命令到新版gcc
sudo ln -sf /usr/bin/gcc-12 /etc/alternatives/cc
```

### 2、禁用开源版显卡驱动

```shell
# 禁用 nouveau
sudo vi /etc/modprobe.d/blacklist.conf
# 结尾处增加两行
blacklist nouveau
options nouveau modeset=0
# 关闭显示服务
sudo telinit 3
# 验证是否禁用了nouveau，显示为空说明成功禁用
lsmod | grep nouveau
```

### 3、下载驱动

```shell
# 驱动下载网址
https://www.nvidia.cn/drivers/lookup/
# 切换下载目录
cd /data
# 下载指定驱动
wget https://cn.download.nvidia.com/tesla/550.90.12/NVIDIA-Linux-x86_64-550.90.12.run
```

### 4、安装驱动

```shell
# 安装程序授执行权限
chmod +x NVIDIA-Linux-x86_64-550.90.12.run
# 安装时有几个warnning，确认即可
sudo ./NVIDIA-Linux-x86_64-550.90.12.run 
# 验证
nvidia-smi
```

## 二、CUDA安装

### 1、下载安装包

```shell
# CUDA首页
https://developer.nvidia.cn/cuda-zone
# 下载链接
https://developer.nvidia.cn/cuda-downloads
# 切换下载目录
cd /data
# 下载安装包
wget https://developer.download.nvidia.com/compute/cuda/12.4.1/local_installers/cuda_12.4.1_550.54.15_linux.run
```

### 2、安装

```shell
# 防止出现临时空间不足的错误，指定一个临时解压目录
# 创建临时目录
mkdir /data/tmp
# 安装
sudo sh cuda_12.4.1_550.54.15_linux.run --tmpdir=/data/tmp/
# 安装时要求确认时输入accept，用方向键选Install
# 增加环境变量
vi ~/.bashrc
# 增加以下两行
export PATH=/usr/local/cuda-12.4/bin:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-12.4/lib64
# 环境变量生效
source ~/.bashrc
# 验证
nvcc -V
```

## 三、Anaconda安装

### 1、下载安装包

```shell
# 下载首页
https://www.anaconda.com/download/success
# 切换下载目录
cd /data
# 下载安装包
wget https://repo.anaconda.com/archive/Anaconda3-2024.06-1-Linux-x86_64.sh
```

### 2、安装

```shell
# 安装程序授执行权限
chmod +x Anaconda3-2024.06-1-Linux-x86_64.sh
# 运行安装包（注意不用sudo）
# 注意事项：1、查看协议用空格键 2、问yes/no时输入yes回车 3、问ENTER时回车
./Anaconda3-2024.06-1-Linux-x86_64.sh
# 使环境变量生效
source ~/.bashrc
# 验证
conda -V
# 此命令显示anaconda的版本号
# 如果报conda命令找不到，则断开ssh重连，以便conda init生效
```

## 四、扩虚拟内存

```shell
# 如果用16G内存的机器运行GLM4-9B，则需要扩充虚拟内容，不然会出现物理内存耗尽的OOM错
# 挂载硬盘
sudo fdisk -l
sudo mkdir /data
sudo mkfs -t ext4 /dev/nvme0n1
sudo mount /dev/nvme0n1 /data
sudo chown -R ubuntu:ubuntu /data
# 扩虚拟内存
sudo swapoff /data/swapfile
sudo dd if=/dev/zero of=/data/swapfile bs=1M count=10240
sudo chmod 0600 /data/swapfile
sudo mkswap /data/swapfile
sudo swapon /data/swapfile
```

