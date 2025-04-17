# ChatPRE: Knowledge-Aware Protocol Analysis with LLMs for Intelligent Segmentation

ChatPRE is a protocol reverse engineering (PRE) tool designed to accurately and precisely perform field inference for protocol messages. This README provides detailed information on its running environment, setup instructions, and usage.

## 1. Running Environment

The following are the main components and requirements for running ChatPRE:

- **Operating System**: Ubuntu 20.04

- **IDA Pro**: IDA Pro 8.3

- **Pin**: Pin 3.28

## 2. Setup Instructions

### 2.1 Prerequisite Installation

First, clone the ChatPRE repository and perform initial setup steps:

```bash
cd ~
git clone https://github.com/huoyuxi/ChatPRE
cd ChatPRE
./install.sh
cd ..
```

**Note**: The ChatPRE - Scaled - [down.py](http://down.py/) is a scaled - down version of ChatPRE that can approximately reproduce the paper results. The full - fledged code will be open - sourced after the paper is accepted.

### 2.2 Starting a Local HTTP Server for Datasets

Navigate to the Dataset directory and start a local HTTP server on port 7777. This is useful for serving the datasets required by ChatPRE.

```bash
cd Dataset
python3 -m http.server 7777
```

### 2.3 Analyzing Protocols Using IDA Pro

Use IDA Pro with the ChatPRE - Scaled - [down.py](http://down.py/) script to analyze different protocols. Replace path\to in the following commands with the actual path to the relevant directories on your system.

```bash
path\to\ida-8.3\idat64 -A -S"path\to\Analyzer\ChatPRE-Scaled-down.py ethernet 0" path\to\Dataset\server\OpENer
path\to\ida-8.3\idat64 -A -S"path\to\Analyzer\ChatPRE-Scaled-down.py ftp 2" path\to\Dataset\server\fftp
path\to\ida-8.3\idat64 -A -S"path\to\Analyzer\ChatPRE-Scaled-down.py http 0" path\to\Dataset\server\miniweb
path\to\ida-8.3\idat64 -A -S"path\to\Analyzer\ChatPRE-Scaled-down.py modbus 1" path\to\Dataset\server\tcpmodbus
path\to\ida-8.3\idat64 -A -S"path\to\Analyzer\ChatPRE-Scaled-down.py s7comm 2"  path\to\Dataset\server\libsnap7.so
path\to\ida-8.3\idat64 -A -S"path\to\Analyzer\ChatPRE-Scaled-down.py tftp 0" path\to\Dataset\server\in.tftpd
```

### 2.4 Special Note for Using ChatPRE-Scaled-down.py

In order to conveniently reproduce the functionality at lines `ChatPRE-Scaled-down.py:614` and `ChatPRE-Scaled-down.py:684`, you need to apply for an API key from [https://siliconflow.cn/zh-cn/models](https://siliconflow.cn/zh-cn/models). Fill in the obtained API key at the `<Token>` position in the relevant code. The models we deployed are all 7b free models, so you can use them with confidence.


### 2.5 Generating Evaluation Files

After protocol analysis, generate the evaluation files by running the following command in the Analyzer directory:

```
cd Analyzer
python3 GenerateChatPreResult.py
```

### 2.6 Evaluation

Perform the evaluation of the generated results using the following command:

```
python3 Evelate.py
```

### 2.7 Expanding the Dataset

To expand the dataset for different protocols, use the following commands. These commands use pin with a pre - loaded library ([libx.so](http://libx.so/)) to instrument the protocol servers.

- **Modbus**:

```bash
sudo LD_PRELOAD=./libx.so pin -t obj-intel64/taint.so -- ./Dataset/server/tcpmodbus
```

- **FFTP**:

```bash
sudo LD_PRELOAD=./libx.so pin -t obj-intel64/taint.so -- ./Dataset/server/fftp ./Dataset/server/fftp.conf
```

- **TFTP**:

```bash
sudo LD_PRELOAD=./libx.so pin -t obj-intel64/taint.so -- ./Dataset/server/tftpd -l -p -s ./Dataset/server
```

- **HTTP**:

```bash
sudo LD_PRELOAD=./libx.so pin -t obj-intel64/taint.so -- ./Dataset/server/miniweb
```

- **S7comm**:

```bash
sudo LD_PRELOAD=./libx.so pin -t obj-intel64/taint.so -- ./Dataset/server/S7comm
```

- **Ethernet**:

```bash
sudo LD_PRELOAD=./libx.so pin -t obj-intel64/taint.so -- ./Dataset/server/OpENer eth0
```
## 3. Customization and Extension

- **Interaction Logic**: The interaction segment requires users to set their own logic according to specific needs.

- **Verification**: For verification purposes, users need to write extensions to the Analyzer\Groundtruth to support new protocols.
