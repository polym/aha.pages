---
cover:
  image: cover.jpg
date: '2025-10-28T12:49:00.000Z'
draft: false
lastmod: '2025-10-29T13:42:00.000Z'
tags:
- Copilot
title: Github Copilot remote-ssh 支持 Claude 系列模型

---

# 背景

# 原因分析

![image](71e5da29_image.png)

# 解决思路

![image](a3f5cd6b_image.png)

1. 在本地 .ssh/config 配置中，找到需要远程连接的主机，增加 RemoteForward 配置。有了这个配置，就会在 ssh 连接时，自动创建端口转发，将 remote 机器上所有请求 7897 端口的流量都转发到 local 机器的 127.0.0.1:7897 上。

	
```json
Host comfy
    HostName ngb1.dc.huixingyun.com
    User root
    Port 53727
    PubkeyAuthentication yes
    IdentityFile ~/.ssh/id_rsa
    RemoteForward 7897 127.0.0.1:7897
```

1. 在 VSCode 的 Remote-ssh 配置中设置 http.proxy

	![image](5fbecc95_image.png)

# 参考资料

1. [VsCode远程Copilot无法使用Claude Agent问题_vscode远程没有claude-CSDN博客](https://blog.csdn.net/qq_40620465/article/details/152000104)

1. [Updating restrictions of sales to unsupported regions](https://www.anthropic.com/news/updating-restrictions-of-sales-to-unsupported-regions)

