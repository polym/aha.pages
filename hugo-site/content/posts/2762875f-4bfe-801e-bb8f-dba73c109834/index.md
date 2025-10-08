---
cover:
  image: cover.jpg
date: '2025-09-22T14:21:00.000Z'
draft: false
lastmod: '2025-10-08T02:33:00.000Z'
tags:
- Hugo
- Notion
title: 使用 Notion-Hugo 构建个人博客

---

## 1. 为什么？

> 为什么会想要构建个人博客并且还是通过 Notion 的方式？

「零秒思考」后的结果：

1. Notion 中毒用户，馋 Notion 的编辑器

1. 对 Notion 中记录的内容做一个系统整理并输出，尽量使用图的形式来展示

1. 记录个人的思考、成长以及展示自己的能力，以便后续回顾

1. 希望每篇博客都有自己的拍摄的一张照片，记录生活的点滴

> 为什么选择 Hugo？

对 Hugo 这个项目接触比较早，大部分代码使用 Golang 实现，后续可操作性更强。

## 2. 架构图

虽然「元否」和 Notion-Hugo 的作者都给出了比较详细的说明，但是在实际配置过程中，还需要熟悉 Github action、Cloudflare builder 等概念，以便理解何时触发网站构建以及发布。梳理了一个架构图以便快速理解原理，为后续优化提供思路。

![image](c81f526b_image.png)

## 3. 遇到的问题

[https://github.com/HEIGE-PCloud/Notion-Hugo](https://github.com/HEIGE-PCloud/Notion-Hugo) 在将 Notion 的 page 转换成 markdown 格式时，如果遇到图片，会将原始 URL 的方式写入到 markdown 文件中，而这个 URL 是有防盗链的，1 小时后便会过期，导致图裂。


```bash
https://prod-files-secure.s3.us-west-2.amazonaws.com/dc681554-1505-4cec-9a8f-844b66d5dcc8/4e9385da-92e0-4c4a-9ba1-871eb116b2e5/DSCF9506_preview.jpeg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466SETVVHQ7%2F20250927%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250927T010113Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBEaCXVzLXdlc3QtMiJHMEUCIBgl6TamR&X-Amz-Signature=d9be103faf2f37cf40ca1481c3dd906b8aa9e47d57bf05b8195d9929f53eebcc&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject
```

考虑到 Notion-Hugo 的转换脚本是通过 nodejs 来实现的，对我来说二开的难度较大，另外整体逻辑也不复杂，最终决定自己来重新搭建一套。在 Github 中找到了多个使用 python 来实现 notion2md 的库，经过对比和少量的 hack，完成了第一版转换脚本：[https://github.com/polym/notion2md](https://github.com/polym/notion2md)

## 4. 其他核心点

以下是 Github Action workflow


```makefile
name: Build and Deploy Blog

on:
  # 每天凌晨 1 点自动触发
  schedule:
    - cron: '0 17 * * *' # 北京时间 01:00
  # 允许手动触发
  workflow_dispatch:

jobs:
  build-deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      # Hugo 主题库拉取
      - name: Update git submodules
        run: |
          git submodule update --init --recursive

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y make
          pip install -r py/requirements.txt

      - name: Install latest Hugo
        run: |
          wget https://github.com/gohugoio/hugo/releases/download/v0.151.0/hugo_0.151.0_linux-amd64.deb -O hugo.deb
          sudo dpkg -i hugo.deb
          hugo version
      
      # 指定 NOTION DB 和 NOTION TOKEN
      - name: Set up environment variables
        run: |
          echo "NOTION_DB_ID=${{ secrets.NOTION_DB_ID }}" > .env
          echo "NOTION_TOKEN=${{ secrets.NOTION_TOKEN }}" >> .env
          echo "NOTION_DB_ID=${{ secrets.NOTION_DB_ID }}" >> $GITHUB_ENV
          echo "NOTION_TOKEN=${{ secrets.NOTION_TOKEN }}" >> $GITHUB_ENV

      - name: Build blog
        run: |
          make convert && make build

      # 自动提交 hugo-site/content 中的内容
      - name: Commit updated content
        uses: stefanzweifel/git-auto-commit-action@v6
        with:
          commit_message: Sync content with Notion
          file_pattern: 'hugo-site/content/'
```

## 5. 后续的思考

- 需要去解决 Notion 中特殊块到 Markdown 的连接

- 对特定 Hugo 主题自定义配置，需要做好适配，初步思路通过 page 的属性字段来实现

<br/>

## 6. 参考资料

- [基于Notion+Hugo搭建博客](https://hugo.happyfou.com/posts/%E5%9F%BA%E4%BA%8Enotion-hugo%E6%90%AD%E5%BB%BA%E5%8D%9A%E5%AE%A2/)

- [https://github.com/HEIGE-PCloud/Notion-Hugo](https://github.com/HEIGE-PCloud/Notion-Hugo)

- [nikvdp.com](https://nikvdp.com/post/a_tool_to_export_notion_pages__hugo-powered_static_sitesblogs/)

- [GitHub - echo724/notion2md: Notion Markdown Exporter with Python Cli](https://github.com/echo724/notion2md)

- [https://github.com/SwordAndTea/notion-to-md-py](https://github.com/SwordAndTea/notion-to-md-py)

<br/>

