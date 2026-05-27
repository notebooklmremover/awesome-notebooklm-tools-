# Awesome NotebookLM 工具集 [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> 精选 Google NotebookLM 工具、脚本和资源合集 — 水印去除、音频处理、提示词工程等。

<p align="center">
  <a href="https://notebooklmremover.org">
    <img src="images/banner.png" alt="NotebookLM Tools" width="800">
  </a>
</p>

<p align="center">
  <strong>🌐 <a href="https://notebooklmremover.org">在线使用 →</a></strong> — 免费、浏览器本地处理、无需上传
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README_ja.md">日本語</a> · <a href="README_ko.md">한국어</a> · <a href="README_es.md">Español</a> · <a href="README_fr.md">Français</a> · <a href="README_de.md">Deutsch</a> · <a href="README_pt.md">Português</a> · <a href="README_ru.md">Русский</a>
</p>

---

## 为什么做这个

Google NotebookLM 是一个强大的 AI 研究工具，能根据文档生成播客、幻灯片、视频和信息图。但免费版会在所有导出内容上添加水印 — 官方去水印需要 NotebookLM Ultra，费用 **$250/月**。

本仓库收集了**免费、开源、隐私优先**的解决方案。

## 目录

- [在线工具](#-在线工具)
- [脚本](#-脚本)
- [水印检测](#-水印检测)
- [Gemini 图片工具](#-gemini-图片工具)
- [音频处理](#-音频处理)
- [元数据与隐私](#️-元数据与隐私)
- [NotebookLM 提示词](#-notebooklm-提示词)
- [资源](#-资源)

---

## 🌐 在线工具

| 工具 | 支持格式 | 隐私 | 免费 |
|------|---------|------|------|
| **[NotebookLM Remover](https://notebooklmremover.org)** | 视频、PDF、PPTX、信息图、Gemini 图片、音频、元数据 | 100% 浏览器本地 | ✅ |
| [SlideClean](https://github.com/aaronyang-ai/slideclean) | PDF | 本地 Python | ✅ |
| [SlideDeckcleaner.com](https://slidedeckcleaner.com) | PDF | 服务器端 | ✅ |

> 💡 **[NotebookLM Remover](https://notebooklmremover.org)** 功能最全面 — 支持 8 种格式，完全在浏览器中通过 WebAssembly 运行，文件绝不离开你的设备。

## 🔍 水印检测

NotebookLM 水印位置固定：

| 格式 | 位置 | 尺寸 (1080p) |
|------|------|-------------|
| 视频 | 右下角 | x=1104, y=656, w=770, h=62 |
| 视频 (720p) | 右下角 | x=736, y=437, w=513, h=41 |
| PDF/PPTX | 右下角 | ~350×80px 扫描区域 |
| 视频结尾 | 最后 2.5 秒 | "Made with Google" 画面 |

### 检测算法

[在线工具](https://notebooklmremover.org) 使用：
1. **连通分量分析** — 在扫描区域检测暗色像素
2. **自适应阈值** — 多轮检测（阈值 80/60/45）
3. **智能过滤** — 按面积、宽高比、位置过滤噪声
4. **梯度填充** — 从周围像素插值还原背景

## ✨ Gemini 图片工具

Gemini AI 图片嵌入了可见的星标水印。去除方式是**数学无损的 alpha 通道反转**：

```
原始像素 = (带水印像素 - α × 255) / (1 - α)
```

该公式完美还原原始像素 — 不是 AI 修复，零质量损失。

**[在线试用 Gemini 去水印 →](https://notebooklmremover.org/gemini-image)**

## 🎵 音频处理

NotebookLM Audio Overview 播客包含片头片尾。去除工具：

- **[NotebookLM 播客剪辑器](https://notebooklmremover.org/audio)** — 浏览器端处理，支持 MP3/M4A/WAV

## 🛡️ 元数据与隐私

AI 生成的图片包含暴露来源的元数据（C2PA、EXIF、XMP）：

- **[图片元数据清理器](https://notebooklmremover.org/metadata)** — 浏览器端处理，清除所有可读元数据

## 📊 免费版 vs Ultra vs NotebookLM Remover

| 功能 | 免费版 | Ultra ($250/月) | NotebookLM Remover |
|------|-------|----------------|-------------------|
| 幻灯片水印 | ✅ 有 | ❌ 无 | ❌ 免费去除 |
| 视频水印 | ✅ 有 | ❌ 无 | ❌ 免费去除 |
| "Made with Google" 片尾 | ✅ 有 | ❌ 无 | ❌ 免费裁剪 |
| 隐私 | 服务器端 | 服务器端 | 100% 浏览器本地 |
| 费用 | 免费 | $250/月 | 免费 |

---

## 贡献

欢迎贡献！查看 [contributing.md](contributing.md)。

## 许可

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](https://creativecommons.org/publicdomain/zero/1.0/)

本作品采用 CC0 1.0 通用许可。
