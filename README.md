# TecentAPI
不基于腾讯云的SDK来调用腾讯云的API

## 1、介绍

使用腾讯云API V3.0加密的方式，通过HTTPS请求来调用腾讯云的API接口，适用一些腾讯云非公开的API接口

## 2、APIConfig 目录

### 2.1 config.py文件

用于存放，API请求的域名地址，接口信息（action信息），以及密钥信息

### 2.2 params文件

用于存放向接口传递的参数信息，部分接口要求传递参数信息（调试模式中的payload信息）

## 3、使用简介

```shell
git clone https://github.com/chuxuan909/TecentAPI.git
```

下载后，修改项目目录，子目录 APIConfig 中的config.py文件和params文件后，python执行文件 wanyong.py

## 4、环境要求

Python 3.X 环境， 2.X环境调用，需要自行修改源码
