#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
update_adblock.py

功能：
1. 下载广告域名列表
2. 生成去重、排序、清理后的 reject-domain.txt
3. 根据 TXT 生成 Sing-box 格式的 reject-domain.json
"""

import requests
import json

# -----------------------------
# 配置：广告列表 URL
# -----------------------------
ADLIST_URL = "https://raw.githubusercontent.com/REIJI007/AdBlock_Rule_For_Sing-box/main/adblock_reject_domain.txt"

# -----------------------------
# Step 1: 下载并生成 reject-domain.txt
# -----------------------------
def generate_txt(url: str, txt_file: str):
    response = requests.get(url)
    response.raise_for_status()
    lines = response.text.splitlines()

    domains = set()
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            # 去掉首尾引号和末尾逗号
            clean_line = line.strip('"').rstrip(',')
            if clean_line:
                domains.add(clean_line)

    domains = sorted(domains)

    with open(txt_file, "w", encoding="utf-8") as f:
        for domain in domains:
            f.write(domain + "\n")

    print(f"TXT 文件生成完成: {txt_file}，共 {len(domains)} 个域名")
    return domains

# -----------------------------
# Step 2: 从 reject-domain.txt 生成 reject-domain.json
# -----------------------------
def generate_json(txt_file: str, json_file: str):
    with open(txt_file, "r", encoding="utf-8") as f:
        domains = [line.strip() for line in f if line.strip()]

    singbox_json = {
        "version": 3,
        "rules": [
            {
                "domain_suffix": domains
            }
        ]
    }

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(singbox_json, f, indent=2, ensure_ascii=False)

    print(f"JSON 文件生成完成: {json_file}，共 {len(domains)} 个域名")

# -----------------------------
# 主程序
# -----------------------------
if __name__ == "__main__":
    TXT_FILE = "reject-domain.txt"
    JSON_FILE = "reject-domain.json"

    # 生成 TXT
    generate_txt(ADLIST_URL, TXT_FILE)

    # 生成 JSON
    generate_json(TXT_FILE, JSON_FILE)
