# 🖼️ Multi Search & LLM Image Downloader

<p align="center">
  <img src="assets/banner.svg" alt="Multi Search & LLM Image Downloader - Bulk Image Scraping for AI" width="100%">
</p>

<p align="center">
  <a href="https://github.com/ishandutta2007/Awesome-Awesome-Awesome"><img src="https://img.shields.io/badge/Awesome-%E2%9C%94-blueviolet?style=flat-square&logo=github" alt="Awesome"/></a>
  <a href="https://pypi.org/project/multi-search-n-llm-image-downloader/"><img src="https://badge.fury.io/py/multi-search-n-llm-image-downloader.svg" alt="PyPI version"/></a>
  <a href="https://pypi.org/project/multi-search-n-llm-image-downloader/"><img src="https://img.shields.io/pypi/pyversions/multi-search-n-llm-image-downloader.svg" alt="Python versions"/></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"/></a>
  <a href="https://github.com/ishandutta2007/multi_search_n_llm_image_downloader/stargazers"><img src="https://img.shields.io/github/stars/ishandutta2007/multi_search_n_llm_image_downloader.svg" alt="GitHub stars"/></a>
  <a href="https://github.com/ishandutta2007/multi_search_n_llm_image_downloader/issues"><img src="https://img.shields.io/github/issues/ishandutta2007/multi_search_n_llm_image_downloader.svg" alt="GitHub issues"/></a>
  <a href="https://github.com/ishandutta2007/multi_search_n_llm_image_downloader"><img src="https://img.shields.io/github/repo-size/ishandutta2007/multi_search_n_llm_image_downloader.svg" alt="Repo Size"/></a>
  <a href="https://github.com/ishandutta2007/multi_search_n_llm_image_downloader"><img src="https://img.shields.io/github/last-commit/ishandutta2007/multi_search_n_llm_image_downloader.svg" alt="Last Commit"/></a>
  <a href="https://github.com/ishandutta2007"><img alt="GitHub followers" src="https://img.shields.io/github/followers/ishandutta2007?label=Follow" /></a>
</p>

🚀 **Multi Search & LLM Image Downloader** is a powerful, high-performance Python tool designed for **bulk image scraping** from Bing, Google, and other search engines. It's the ultimate solution for building **large-scale datasets** for **Machine Learning**, **Deep Learning**, **Computer Vision**, and **Generative AI (LLM)** projects. Whether you need an **image dataset downloader** or an automated **web scraping bot**, this library offers speed and flexibility.

---

## 🚀 Key Features

- 🔍 **Multi-Engine Support:** Download images from Bing and Google (and more to come!).
- ⚡ **Lightning Fast:** Parallel downloading using multi-threading for maximum performance.
- 🛠️ **Highly Customizable:** Filter by image type, color, size, and more.
- 🤖 **LLM & AI Ready:** Ideal for gathering training data for AI models.
- 💻 **Flexible Interface:** Use it as a Python library or via the Command Line Interface (CLI).
- 🌐 **Robust Scraping:** Supports both API-based and browser-based (Selenium) retrieval.
- 🕵️ **Stealthy & Safe:** Includes proxy support and headless browser options.
- 📦 **Easy Integration:** Simple installation via pip.

---

## 📚 Table of Contents

- [📍 Quick Start](#-quick-start)
- [⚙️ Installation](#️-installation)
- [🖥️ Usage](#️-usage)
  - [🐍 Python API](#-python-api)
  - [📟 Command Line Interface](#-command-line-interface)
- [🔧 Parameters](#-parameters)
- [💡 Examples](#-examples)
- [🤝 Contributing](#-contributing)
- [⚖️ License](#️-license)
- [⚠️ Disclaimer](#️-disclaimer)
- [📝 Changelog](#-changelog)
- [📧 Contact](#-contact)

---

## 📍 Quick Start

```bash
pip install multi-search-n-llm-image-downloader
python -m multi_downloader.multidownloader "neon cityscapes" --engine "Google" --max-number 10
```

---

## ⚙️ Installation

### Using pip 📦

```bash
pip install multi-search-n-llm-image-downloader
```

### From source 🛠️

```bash
git clone https://github.com/ishandutta2007/multi_search_n_llm_image_downloader
cd multi_search_n_llm_image_downloader
python -m venv ./env
# On Windows: env\Scripts\activate | On Unix: source env/bin/activate
pip install -e .
```

---

## 🖥️ Usage

### 🐍 Python API

```python
from multi_downloader import downloader

# Basic usage: Download 50 puppy images
downloader("cute puppies", limit=50)

# Advanced usage: Filtered download with parallel threads
downloader(
    query="futuristic architecture",
    limit=100,
    output_dir="dataset/architecture",
    filter="photo",  # Options: "line", "photo", "clipart", "gif", "transparent"
    max_workers=8,   # Parallel downloads
    engine="google"
)
```

### 📟 Command Line Interface

The package provides two CLI modes for flexibility:

#### 1️⃣ Simple CLI (Bing-only)
```bash
python -m multi_downloader.download "cyberpunk aesthetic" --limit 20
```

#### 2️⃣ Advanced CLI (Bing & Google)
```bash
python -m multi_downloader.multidownloader "vintage cars" --engine "Google" --max-number 50 --type "photograph"
```

---

## 🔧 Parameters

### Python API Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `query` | str | (req) | Search term |
| `limit` | int | 100 | Max images to download |
| `output_dir` | str | 'dataset' | Save directory |
| `filter` | str | "" | Type (line, photo, clipart, gif, transparent) |
| `max_workers` | int | 4 | Number of parallel threads |
| `engine` | str | "bing" | Search engine to use |

### CLI Arguments (`multidownloader.py`)

| Argument | Short | Default | Description |
| :--- | :--- | :--- | :--- |
| `--engine` | `-e` | "Bing" | "Google" or "Bing" |
| `--driver` | `-d` | "firefox_headless" | Browser driver |
| `--max-number` | `-n` | 100 | Max images |
| `--num-threads` | `-j` | 50 | Concurrent threads |
| `--output` | `-o` | "./download_images" | Output path |
| `--type` | `-ty` | None | clipart, linedrawing, photograph |

---

## 💡 Examples

### 🖼️ Bulk Download for Dataset
```bash
python -m multi_downloader.multidownloader "forest landscapes" -e "Google" -n 200 -o "./datasets/forests"
```

### 🎨 Download Transparent Clipart
```python
downloader(query="star icon", limit=20, filter="transparent", engine="google")
```

---

## 🧪 Running Tests

To ensure the package and its features work as expected, you can run the provided test suite using `pytest`.

1. **Install Test Dependencies** (if not already installed):
```bash
pip install pytest
```

2. **Run Tests**:
Execute the tests from the root of the project directory:
```bash
pytest tests/
```
The test suite heavily utilizes mocking to ensure tests run fast and without requiring internet or browser dependencies.

---

## 🤝 Contributing

Contributions are welcome! If you have a feature request, bug report, or want to improve the code, please open an issue or submit a pull request. 

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## ⚖️ License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

## ⚠️ Disclaimer

This tool is for educational and research purposes. Please respect the copyright of the images you download and the Terms of Service of the search engines. The developers are not responsible for any misuse.

---

## 📝 Changelog

### 🚀 0.1.0
- Refactored project structure.
- Improved CLI performance.
- Added support for more browser drivers.

---

## 📧 Contact

**Ishan Dutta** - [ishandutta2007@gmail.com](mailto:ishandutta2007@gmail.com)

Project Link: [https://github.com/ishandutta2007/multi_search_n_llm_image_downloader](https://github.com/ishandutta2007/multi_search_n_llm_image_downloader)

---

<p align="center">
  <a href="https://github.com/ishandutta2007/multi_search_n_llm_image_downloader">
    <img src="https://api.star-history.com/svg?repos=ishandutta2007/multi_search_n_llm_image_downloader&type=Date" alt="Star History Chart">
  </a>
</p>
