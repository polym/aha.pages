---
cover:
  image: cover.jpg
date: '2025-09-22T14:21:00.000Z'
draft: false
lastmod: '2025-09-27T14:03:00.000Z'
tags: []
title: 使用 Notion-Hugo 构建个人博客

---

## 1. 为什么？

> 为什么会想要构建个人博客并且还是通过 Notion 的方式？

「零秒思考」后的结果：

1. 对 Notion 中记录的内容做一个系统整理并输出，尽量使用图的形式来展示

1. 记录个人的思考、成长以及展示自己的能力，以便后续回顾

1. 希望每篇博客都有自己的拍摄的一张照片，记录生活的点滴

> 为什么选择 Hugo？

对 Hugo 这个项目接触比较早，大部分代码使用 Golang 实现，后续可操作性更强。

## 2. 架构图

虽然「元否」和 Notion-Hugo 的作者都给出了比较详细的说明，但是在实际配置过程中，还需要熟悉 Github action、Cloudflare builder 等概念，以便理解何时触发网站构建以及发布。梳理了一个架构图以便快速理解原理，为后续优化提供思路。

![image](c81f526b_image.png)

## 3. 参考资料

- [基于Notion+Hugo搭建博客](https://hugo.happyfou.com/posts/%E5%9F%BA%E4%BA%8Enotion-hugo%E6%90%AD%E5%BB%BA%E5%8D%9A%E5%AE%A2/)

- [https://github.com/HEIGE-PCloud/Notion-Hugo](https://github.com/HEIGE-PCloud/Notion-Hugo)

