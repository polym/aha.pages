---
cover:
  image: cover.jpg
date: '2025-10-28T09:31:00.000Z'
draft: true
lastmod: '2025-11-03T13:37:00.000Z'
tags: []
title: '容器镜像压缩 Gzip vs Zstd vs Pigz '

---

## 背景

众所周知，

<br/>

> [https://docs.docker.com/build/exporters/image-registry/](https://docs.docker.com/build/exporters/image-registry/)

uncompressed

62.55GiB

time docker pull [ngb1h.dc.huixingyun.com/huixingyun/comfyui@sha256:ada3be1b43a5cbee034e4c1c22f92162a4110d85734543728c0087f6f39e3c02](http://ngb1h.dc.huixingyun.com/huixingyun/comfyui@sha256:ada3be1b43a5cbee034e4c1c22f92162a4110d85734543728c0087f6f39e3c02)

![image](c4acdae8_image.png)

real    8m20.121s
user    0m0.645s
sys     0m0.494s

<br/>

gzip

34.43GiB

time docker pull [ngb1h.dc.huixingyun.com/huixingyun/comfyui@sha256:15bdc7348ef74a91e32486f721943691fd4a7a1d257ecd44c1a888fc12fd79b8](http://ngb1h.dc.huixingyun.com/huixingyun/comfyui@sha256:15bdc7348ef74a91e32486f721943691fd4a7a1d257ecd44c1a888fc12fd79b8)

![image](e92a524d_image.png)

real    15m38.304s
user    0m0.611s
sys     0m0.569s

<br/>

pigz

real    7m50.097s
user    0m0.468s
sys     0m0.310s

<br/>

zstd

29.70GiB

time docker pull [ngb1h.dc.huixingyun.com/huixingyun/comfyui@sha256:468a5e990ca263ce3012f33ef740b2957f3e98dfe67416c3ae023eb24f857c5b](http://ngb1h.dc.huixingyun.com/huixingyun/comfyui@sha256:468a5e990ca263ce3012f33ef740b2957f3e98dfe67416c3ae023eb24f857c5b)

![image](d5d29a6d_image.png)

real    5m27.149s
user    0m0.332s
sys     0m0.312s

<br/>

zstd > uncompressed > gzip

1. 为什么 zstd 比 uncompressed？

	uncompressed 的大小是 zstd 的两倍，意味着巨大的 I/O 读取量。zstd 飞速的解压可以保证读取、解包、写入 磁盘高度并行化。

1. 为什么 gzip 最慢？

	gzip 解压是单核处理的效率比较低。

