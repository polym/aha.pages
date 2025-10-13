---
cover:
  image: cover.jpg
date: '2025-10-13T12:22:00.000Z'
draft: true
lastmod: '2025-10-13T14:41:00.000Z'
tags:
- AI
- PyTorch
title: fp8 量化的几种姿势

---

# 背景

今年以来，在图像视频领域，开源的 AIGC 模型参数规模越来越大，例如，QwenImage 达到了 20B，Wan2.2 达到了 27B（High-Noise 和 Low-Noise 专家各占用 14B）。参数规模越大，就意味着需要更多的显存来加载模型，需要更多的算力来进行模型推理。而此时如果你想将这些 SOTA 模型运行在更加经济的消费级显卡时，就需要对模型进行量化（可以理解为压缩）。对于一张 24GB 显存的 4090 显卡而言，如果想要加载 QwenImage 模型，就必须将模型权重量化到 fp8 精度。如果采用 fp8 精度，模型显存占用粗略估算如下，可以放到 24GB 显存中：


```makefile
num_params = 20 * 2^30
fp8_size = 1 byte

total_size = num_params * fp8_size = 20 * 2^30 * 1 byte = 20 GBytes
```

正好最近发现模型训练工具 musubi-tuner 作者正在比较不同 fp8 量化方式对图片生成结果的影响，以及对 ComfyUI 模型精度 fp8_e4m3、fp8_e5m2、fp8_e3m2_fast 的一知半解，决定做一次系统的学习与整理。

# 精度与量化

![image](2451d8b9_image.png)

浮点精度相信大家都不陌生，只不过接触比较多可能是 float32 单精度浮点数或者 float64 双精度浮点数。简单来说，浮点数的表示分为「符号位」、「指数位」、「尾数位」，如上图所示，其中每个色块代表一个 bit。你会发现 float8 精度有两个表示方式，fp8_e4m3 和 fp8_e5m2，不同的表示意味着不同的取值范围，fp8_e5m2 范围为 [-2^15, 2^15]，而 fp8_e4m3 只有 [-2^7, 2^7]。

而所谓的量化，其实是将数值从较大的精度范围（bf16）缩小到较小的精度范围（fp8_e4m3）；反量化则刚好相反。

# FP8 的几种量化方式

![image](1bd779f1_image.png)

将 bf16 精度的数值量化到 fp8_e5m2 精度，有以下 3 种方式：

1. Cast-To：该方法不属于量化范畴，只是简单的数值转换。可以发现灰色部分会被直接映射到最小或最大值上。

1. Tensor-wise FP8 量化：对于每个 Tensor（模型是由多个 Tensor 组成，Tensor 中包含一组参数），找出当前参数数值的最小取值范围，并将这个范围映射到 fp8 的范围内。该过程就是量化，其中映射过程会有一个缩放因子，通过缩放因子可以对参数进行反量化。

1. Block-wise FP8 量化：将每个 Tensor 按照固定 block 大小切分成多个 block，在对 block 中的参数按 Tensor-wise 的方法进行量化，区别在于每个 block 会有一个缩放因子。这个方法粒度更细，精度相对会更高。

# Tensor-wise FP8 量化模型布局比较

![image](183b795f_image.png)

# 细粒度量化 (Fine-grained quantization)

> HuggingFace transformers 库中提供了对 block-wise fp8 量化方式的支持

![image](31de6eec_image.png)

# 参考资料

- [Wan-AI/Wan2.2-T2V-A14B · Hugging Face](https://huggingface.co/Wan-AI/Wan2.2-T2V-A14B)

- [https://huggingface.co/docs/transformers/en/quantization/finegrained_fp8](https://huggingface.co/docs/transformers/en/quantization/finegrained_fp8)

<br/>

