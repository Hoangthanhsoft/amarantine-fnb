# 🦐 Amarantine AI — F&B Ops System

> AI-powered content production engine for multi-venue F&B operators.  
> Built for Australian hospitality groups. Open source core. Production-ready.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)

## 🚀 What it does

Input: One promotional brief (e.g. *"Half-price oysters every Friday 5–7pm"*)  
Output in ~8 seconds:

| Asset | Count |
|---|---|
| Facebook posts (3 angles) | 3 |
| Instagram caption + hashtags | 1 + 5 |
| Email subject lines | 3 |
| Email body | 1 |
| Video scripts (15s + 30s) | 2 |
| Signage headline + subline | 1 |
| Menu description | 1 |
| Midjourney photo prompt | 1 |
| Web copy | 1 |
| **Total** | **~19 assets** |

## ⚡ Quick Start (3 commands)

```bash
git clone https://github.com/Hoangthanhsoft/amarantine-fnb
cd amarantine-fnb
cp .env.example .env   # add your API keys
docker-compose up
