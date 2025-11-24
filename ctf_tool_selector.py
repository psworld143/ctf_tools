#!/usr/bin/env python3
"""
Interactive selector for common CTF tooling referenced by the Windows
installer batch scripts. Presents a quick reference and can launch the
tool with user-specified arguments when it is available on PATH or in
installation folders. Includes intelligent challenge type detection.
"""

from __future__ import annotations

import os
import platform
import shlex
import shutil
import subprocess
from textwrap import dedent
from typing import Any

try:
    import requests
except ImportError:
    requests = None


def get_windows_install_paths() -> dict[str, list[str]]:
    """Return mapping of tool commands to their Windows installation paths."""
    user_profile = os.environ.get("USERPROFILE", os.environ.get("HOME", ""))
    toolkit_root = os.path.join(user_profile, "Desktop", "CTF-Toolkit")
    
    return {
        "exiftool": [
            r"C:\Program Files\Exiftool\exiftool.exe",
            os.path.join(toolkit_root, "Tools-Binaries", "exiftool", "exiftool.exe"),
        ],
        "binwalk": [
            r"C:\ProgramData\chocolatey\bin\binwalk.exe",
            os.path.join(toolkit_root, "Tools-Binaries", "binwalk", "binwalk.exe"),
        ],
        "zsteg": [
            r"C:\tools\ruby31\bin\zsteg.bat",
            os.path.join(toolkit_root, "Tools-Binaries", "zsteg", "zsteg.bat"),
        ],
        "hashcat": [
            r"C:\Program Files\hashcat\hashcat.exe",
            os.path.join(toolkit_root, "Tools-Binaries", "hashcat", "hashcat.exe"),
        ],
        "john": [
            r"C:\Program Files\John\run\john.exe",
            os.path.join(toolkit_root, "Tools-Binaries", "john", "john.exe"),
        ],
        "strings": [
            r"C:\Program Files\GnuWin32\bin\strings.exe",
            os.path.join(toolkit_root, "Tools-Binaries", "utilities", "strings.exe"),
        ],
        "xxd": [
            r"C:\Program Files\GnuWin32\bin\xxd.exe",
            os.path.join(toolkit_root, "Tools-Binaries", "utilities", "xxd.exe"),
        ],
        "ncat": [
            r"C:\Program Files (x86)\Nmap\ncat.exe",
            r"C:\Program Files\Nmap\ncat.exe",
            os.path.join(toolkit_root, "Tools-Binaries", "utilities", "ncat.exe"),
        ],
        "curl": [
            r"C:\Windows\System32\curl.exe",
            os.path.join(toolkit_root, "Tools-Binaries", "utilities", "curl.exe"),
        ],
        "ghidraRun": [
            r"C:\Program Files\ghidra\ghidraRun.bat",
            os.path.join(toolkit_root, "Tools-Binaries", "ghidra", "ghidraRun.bat"),
        ],
        "radare2": [
            r"C:\ProgramData\chocolatey\bin\radare2.exe",
            os.path.join(toolkit_root, "Tools-Binaries", "radare2", "radare2.exe"),
        ],
        "wireshark": [
            r"C:\Program Files\Wireshark\Wireshark.exe",
            os.path.join(toolkit_root, "Tools-Binaries", "wireshark", "Wireshark.exe"),
        ],
        "burpsuite": [
            r"C:\Program Files\BurpSuiteCommunity\burpsuite_community.exe",
            r"C:\Program Files\Burp Suite Community Edition\burpsuite_community.exe",
        ],
        "burpsuitecommunity": [
            r"C:\Program Files\BurpSuiteCommunity\burpsuite_community.exe",
            r"C:\Program Files\Burp Suite Community Edition\burpsuite_community.exe",
        ],
        "cyberchef": [
            r"C:\Program Files\CyberChef\CyberChef.exe",
            r"C:\Users\{}\AppData\Local\Programs\CyberChef\CyberChef.exe".format(
                os.environ.get("USERNAME", "")
            ),
        ],
    }


# Hardcoded AI Providers (enabled providers from ai_providers.sql, sorted by priority)
AI_PROVIDERS: list[dict[str, Any]] = [
    {
        'id': 4,
        'name': 'azure',
        'display_name': 'Azure OpenAI',
        'provider_type': 'azure',
        'api_url': 'https://pswor-mf5h1ule-eastus2.cognitiveservices.azure.com/openai/deployments/gpt-35-turbo/chat/completions?api-version=2025-01-01-preview',
        'model': 'gpt-35-turbo',
        'api_key': '4paawf7p9EfUZDUozhpZr0XpEgneiGuWEPyPXucTWFYNcOH6AaRIJQQJ99BIACHYHv6XJ3w3AAAAACOGhacj',
        'max_tokens': 4000,
        'temperature': 0.0,
        'enabled': 1,
        'priority': 6,
        'description': 'Azure OpenAI model for generating quiz questions',
        'instructions': 'You are an expert educational content creator specializing in creating high-quality quiz questions based on educational materials.',
    },
    {
        'id': 28,
        'name': 'groq_kimi_k2',
        'display_name': 'Groq Kimi K2 Instruct',
        'provider_type': 'openai',
        'api_url': 'https://api.groq.com/openai/v1/chat/completions',
        'model': 'moonshotai/kimi-k2-instruct',
        'api_key': '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',
        'max_tokens': 16384,
        'temperature': 0.7,
        'enabled': 1,
        'priority': 6,
        'description': 'Groq Kimi K2 Instruct - Moonshot AI model with 131K context window',
        'instructions': 'You are an expert academic curriculum designer specializing in Philippine higher education standards and CHED (Commission on Higher Education) guidelines.',
    },
    {
        'id': 29,
        'name': 'groq_gpt_oss_20b',
        'display_name': 'Groq GPT-OSS 20B',
        'provider_type': 'openai',
        'api_url': 'https://api.groq.com/openai/v1/chat/completions',
        'model': 'openai/gpt-oss-20b',
        'api_key': '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',
        'max_tokens': 65536,
        'temperature': 0.7,
        'enabled': 1,
        'priority': 7,
        'description': 'Groq GPT-OSS 20B - OpenAI open source model with 131K context window',
        'instructions': 'You are an expert academic curriculum designer specializing in Philippine higher education standards and CHED (Commission on Higher Education) guidelines.',
    },
    {
        'id': 30,
        'name': 'groq_gemma2_9b',
        'display_name': 'Groq Gemma 2 9B',
        'provider_type': 'openai',
        'api_url': 'https://api.groq.com/openai/v1/chat/completions',
        'model': 'gemma2-9b-it',
        'api_key': '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',
        'max_tokens': 8192,
        'temperature': 0.7,
        'enabled': 1,
        'priority': 8,
        'description': 'Groq Gemma 2 9B - Google model with 8K context window',
        'instructions': 'You are an expert academic curriculum designer specializing in Philippine higher education standards and CHED (Commission on Higher Education) guidelines.',
    },
    {
        'id': 31,
        'name': 'groq_allam_2_7b',
        'display_name': 'Groq Allam 2 7B',
        'provider_type': 'openai',
        'api_url': 'https://api.groq.com/openai/v1/chat/completions',
        'model': 'allam-2-7b',
        'api_key': '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',
        'max_tokens': 4096,
        'temperature': 0.7,
        'enabled': 1,
        'priority': 9,
        'description': 'Groq Allam 2 7B - SDAIA model with 4K context window',
        'instructions': 'You are an expert academic curriculum designer specializing in Philippine higher education standards and CHED (Commission on Higher Education) guidelines.',
    },
    {
        'id': 32,
        'name': 'groq_llama_4_scout',
        'display_name': 'Groq LLaMA 4 Scout 17B',
        'provider_type': 'openai',
        'api_url': 'https://api.groq.com/openai/v1/chat/completions',
        'model': 'meta-llama/llama-4-scout-17b-16e-instruct',
        'api_key': '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',
        'max_tokens': 8192,
        'temperature': 0.7,
        'enabled': 1,
        'priority': 10,
        'description': 'Groq LLaMA 4 Scout 17B - Meta model with 131K context window',
        'instructions': 'You are an expert academic curriculum designer specializing in Philippine higher education standards and CHED (Commission on Higher Education) guidelines.',
    },
    {
        'id': 33,
        'name': 'groq_gpt_oss_120b',
        'display_name': 'Groq GPT-OSS 120B',
        'provider_type': 'openai',
        'api_url': 'https://api.groq.com/openai/v1/chat/completions',
        'model': 'openai/gpt-oss-120b',
        'api_key': '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',
        'max_tokens': 65536,
        'temperature': 0.7,
        'enabled': 1,
        'priority': 11,
        'description': 'Groq GPT-OSS 120B - Large OpenAI open source model with 131K context window',
        'instructions': 'You are an expert academic curriculum designer specializing in Philippine higher education standards and CHED (Commission on Higher Education) guidelines.',
    },
    {
        'id': 34,
        'name': 'groq_deepseek_r1',
        'display_name': 'Groq DeepSeek R1 Distill',
        'provider_type': 'openai',
        'api_url': 'https://api.groq.com/openai/v1/chat/completions',
        'model': 'deepseek-r1-distill-llama-70b',
        'api_key': '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',
        'max_tokens': 131072,
        'temperature': 0.7,
        'enabled': 1,
        'priority': 12,
        'description': 'Groq DeepSeek R1 Distill - DeepSeek reasoning model with 131K context window',
        'instructions': 'You are an expert academic curriculum designer specializing in Philippine higher education standards and CHED (Commission on Higher Education) guidelines.',
    },
    {
        'id': 35,
        'name': 'groq_llama_33_70b',
        'display_name': 'Groq LLaMA 3.3 70B',
        'provider_type': 'openai',
        'api_url': 'https://api.groq.com/openai/v1/chat/completions',
        'model': 'llama-3.3-70b-versatile',
        'api_key': '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',
        'max_tokens': 32768,
        'temperature': 0.7,
        'enabled': 1,
        'priority': 13,
        'description': 'Groq LLaMA 3.3 70B - Latest Meta model with 131K context window',
        'instructions': 'You are an expert academic curriculum designer specializing in Philippine higher education standards and CHED (Commission on Higher Education) guidelines.',
    },
    {
        'id': 26,
        'name': 'groq_qwen_32b',
        'display_name': 'Groq Qwen 3 32B',
        'provider_type': 'openai',
        'api_url': 'https://api.groq.com/openai/v1/chat/completions',
        'model': 'qwen/qwen3-32b',
        'api_key': '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',
        'max_tokens': 40960,
        'temperature': 0.7,
        'enabled': 1,
        'priority': 14,
        'description': 'Groq Qwen 3 32B - Alibaba Cloud model with 131K context window',
        'instructions': 'You are an expert academic curriculum designer specializing in Philippine higher education standards and CHED (Commission on Higher Education) guidelines.',
    },
    {
        'id': 22,
        'name': 'groq_llama_70b',
        'display_name': 'Groq LLaMA 3.1 70B',
        'provider_type': 'openai',
        'api_url': 'https://api.groq.com/openai/v1/chat/completions',
        'model': 'llama-3.1-8b-instant',
        'api_key': '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',
        'max_tokens': 131072,
        'temperature': 0.7,
        'enabled': 1,
        'priority': 15,
        'description': 'Groq LLaMA 3.1 8B Instant - Fast inference with 131K context window, free tier available',
        'instructions': 'You are an expert academic curriculum designer specializing in Philippine higher education standards and CHED (Commission on Higher Education) guidelines.',
    },
    {
        'id': 12,
        'name': 'google_gemini_25_pro',
        'display_name': 'Google Gemini 2.5 Pro',
        'provider_type': 'google',
        'api_url': 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent',
        'model': 'gemini-2.5-pro',
        'api_key': 'AIzaSyBzRvmQNNmTaFoDanA3VChM7I1za3YRftc',
        'max_tokens': 1000000,
        'temperature': 0.7,
        'enabled': 1,
        'priority': 20,
        'description': 'Google Gemini 2.5 Pro with 1M context window - latest model with enhanced reasoning capabilities',
        'instructions': 'You are an expert academic curriculum designer specializing in Philippine higher education standards and CHED (Commission on Higher Education) guidelines.',
    },
    {
        'id': 13,
        'name': 'google_gemini_20_flash',
        'display_name': 'Google Gemini 2.0 Flash',
        'provider_type': 'google',
        'api_url': 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent',
        'model': 'gemini-2.0-flash',
        'api_key': 'AIzaSyBzRvmQNNmTaFoDanA3VChM7I1za3YRftc',
        'max_tokens': 1000000,
        'temperature': 0.7,
        'enabled': 1,
        'priority': 21,
        'description': 'Google Gemini 2.0 Flash with 1M context window - fast and efficient for large tasks',
        'instructions': 'You are an expert academic curriculum designer specializing in Philippine higher education standards and CHED (Commission on Higher Education) guidelines.',
    },
    {
        'id': 3,
        'name': 'google',
        'display_name': 'Google Gemini',
        'provider_type': 'google',
        'api_url': 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent',
        'model': 'gemini-1.5-flash',
        'api_key': 'AIzaSyBzRvmQNNmTaFoDanA3VChM7I1za3YRftc',
        'max_tokens': 1000000,
        'temperature': 0.0,
        'enabled': 1,
        'priority': 22,
        'description': 'Google Gemini 1.5 Flash with 1M context window - fast and efficient',
        'instructions': 'You are an expert educational content creator specializing in creating high-quality quiz questions based on educational materials.',
    },
    {
        'id': 36,
        'name': 'groq_compound',
        'display_name': 'Groq Compound',
        'provider_type': 'openai',
        'api_url': 'https://api.groq.com/openai/v1/chat/completions',
        'model': 'groq/compound',
        'api_key': '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',
        'max_tokens': 8192,
        'temperature': 0.7,
        'enabled': 1,
        'priority': 24,
        'description': 'Groq Compound - Groq proprietary model with 131K context window',
        'instructions': 'You are an expert academic curriculum designer specializing in Philippine higher education standards and CHED (Commission on Higher Education) guidelines.',
    },
    {
        'id': 23,
        'name': 'groq_mixtral',
        'display_name': 'Groq Mixtral 8x7B',
        'provider_type': 'openai',
        'api_url': 'https://api.groq.com/openai/v1/chat/completions',
        'model': 'llama-3.1-8b-instant',
        'api_key': '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',
        'max_tokens': 32768,
        'temperature': 0.7,
        'enabled': 1,
        'priority': 26,
        'description': 'Groq LLaMA 3.1 8B Instant - Fast inference with 32K context window, excellent for general tasks',
        'instructions': 'You are an expert academic curriculum designer specializing in Philippine higher education standards and CHED (Commission on Higher Education) guidelines.',
    },
    {
        'id': 24,
        'name': 'groq_gemma',
        'display_name': 'Groq Gemma 7B',
        'provider_type': 'openai',
        'api_url': 'https://api.groq.com/openai/v1/chat/completions',
        'model': 'llama-3.1-8b-instant',
        'api_key': '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',
        'max_tokens': 8192,
        'temperature': 0.7,
        'enabled': 1,
        'priority': 27,
        'description': 'Groq LLaMA 3.1 8B Instant - Fast and efficient model with 8K context window, free tier available',
        'instructions': 'You are an expert academic curriculum designer specializing in Philippine higher education standards and CHED (Commission on Higher Education) guidelines.',
    },
    {
        'id': 37,
        'name': 'openrouter_gpt35',
        'display_name': 'OpenRouter GPT-3.5-turbo',
        'provider_type': 'openrouter',
        'api_url': 'https://openrouter.ai/api/v1/chat/completions',
        'model': 'openai/gpt-3.5-turbo',
        'api_key': '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',
        'max_tokens': 4000,
        'temperature': 0.7,
        'enabled': 1,
        'priority': 50,
        'description': 'OpenRouter access to OpenAI GPT-3.5-turbo - cost-effective alternative',
        'instructions': 'You are an expert educational content creator specializing in creating high-quality quiz questions based on educational materials.',
    },
    {
        'id': 39,
        'name': 'openrouter_claude_sonnet',
        'display_name': 'OpenRouter Claude 3.5 Sonnet',
        'provider_type': 'openrouter',
        'api_url': 'https://openrouter.ai/api/v1/chat/completions',
        'model': 'anthropic/claude-3.5-sonnet',
        'api_key': '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',
        'max_tokens': 200000,
        'temperature': 0.7,
        'enabled': 1,
        'priority': 52,
        'description': 'OpenRouter access to Anthropic Claude 3.5 Sonnet - excellent balance of intelligence and speed',
        'instructions': 'You are an expert educational content creator specializing in creating high-quality quiz questions based on educational materials.',
    },
    {
        'id': 41,
        'name': 'openrouter_llama_70b',
        'display_name': 'OpenRouter LLaMA 3.1 70B',
        'provider_type': 'openrouter',
        'api_url': 'https://openrouter.ai/api/v1/chat/completions',
        'model': 'meta-llama/llama-3.1-70b-instruct',
        'api_key': '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',
        'max_tokens': 131072,
        'temperature': 0.7,
        'enabled': 1,
        'priority': 54,
        'description': 'OpenRouter access to Meta LLaMA 3.1 70B - powerful open-source model',
        'instructions': 'You are an expert educational content creator specializing in creating high-quality quiz questions based on educational materials.',
    },
    {
        'id': 43,
        'name': 'openrouter_deepseek',
        'display_name': 'OpenRouter DeepSeek Chat',
        'provider_type': 'openrouter',
        'api_url': 'https://openrouter.ai/api/v1/chat/completions',
        'model': 'deepseek/deepseek-chat',
        'api_key': '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',
        'max_tokens': 32000,
        'temperature': 0.7,
        'enabled': 1,
        'priority': 56,
        'description': 'OpenRouter access to DeepSeek Chat - excellent for code and reasoning tasks',
        'instructions': 'You are an expert educational content creator specializing in creating high-quality quiz questions based on educational materials.',
    },
]


def get_best_ai_provider() -> dict[str, Any] | None:
    """Get the highest priority enabled AI provider."""
    # Providers are already sorted by priority (lower = higher priority)
    return AI_PROVIDERS[0] if AI_PROVIDERS else None


def analyze_file_with_ai(file_path: str, provider: dict[str, Any] | None = None) -> str | None:
    """Analyze a file to determine CTF challenge type."""
    if requests is None:
        print("[!] 'requests' library not installed. Install with: pip install requests")
        return None
    
    if provider is None:
        provider = get_best_ai_provider()
        if provider is None:
            print("[!] Analysis engine not available. Please check configuration.")
            return None
    
    if not os.path.exists(file_path):
        print(f"[!] File not found: {file_path}")
        return None
    
    try:
        # Read file content
        file_size = os.path.getsize(file_path)
        file_ext = os.path.splitext(file_path)[1].lower()
        
        # For small text files, read content directly
        # For binary/large files, provide metadata
        file_content = None
        file_info = f"File: {os.path.basename(file_path)}\nSize: {file_size} bytes\nExtension: {file_ext}\n"
        
        if file_size < 100000:  # Read files < 100KB
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    file_content = f.read()[:50000]  # Limit to 50KB
                file_info += f"\nContent preview:\n{file_content[:2000]}"
            except:
                # Binary file - read as hex
                with open(file_path, 'rb') as f:
                    file_bytes = f.read(1024)
                    file_info += f"\nHex preview:\n{file_bytes.hex()[:500]}"
        else:
            # Large file - just metadata
            file_info += f"\n(Large file - analyzing metadata only)"
        
        # Prepare analysis prompt
        prompt = f"""Analyze this CTF challenge file and determine:
1. Challenge category (Forensics, Steganography, Cryptography, Reverse Engineering, Web, Misc, etc.)
2. Likely file type and format
3. Recommended tools to use
4. Initial analysis steps
5. Potential flags or hidden data locations

{file_info}

Provide a concise analysis with specific tool recommendations from this CTF toolkit:
- ExifTool (metadata)
- Binwalk (embedded files)
- zsteg (steganography)
- Hashcat/John (cracking)
- strings/xxd (binary analysis)
- Ghidra/radare2 (reverse engineering)
- Wireshark (network analysis)
"""
        
        # Call analysis engine based on provider type
        if provider['provider_type'] == 'openai':
            return call_openai_api(provider, prompt)
        elif provider['provider_type'] == 'anthropic':
            return call_anthropic_api(provider, prompt)
        elif provider['provider_type'] == 'google':
            return call_google_api(provider, prompt)
        elif provider['provider_type'] == 'openrouter':
            return call_openrouter_api(provider, prompt)
        else:
            print(f"[!] Unsupported provider type: {provider['provider_type']}")
            return None
    
    except Exception as e:
        print(f"[!] Error analyzing file: {e}")
        return None


def call_openai_api(provider: dict[str, Any], prompt: str) -> str | None:
    """Call OpenAI-compatible API."""
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {provider['api_key']}"
        }
        
        data = {
            'model': provider['model'],
            'messages': [
                {'role': 'system', 'content': provider.get('instructions', 'You are a CTF expert.')},
                {'role': 'user', 'content': prompt}
            ],
            'max_tokens': min(provider.get('max_tokens', 4000), 4000),
            'temperature': provider.get('temperature', 0.7)
        }
        
        response = requests.post(provider['api_url'], headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        print(f"[!] OpenAI API error: {e}")
        return None


def call_anthropic_api(provider: dict[str, Any], prompt: str) -> str | None:
    """Call Anthropic Claude API."""
    try:
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': provider['api_key'],
            'anthropic-version': '2023-06-01'
        }
        
        data = {
            'model': provider['model'],
            'max_tokens': min(provider.get('max_tokens', 200000), 4096),
            'messages': [
                {'role': 'user', 'content': f"{provider.get('instructions', '')}\n\n{prompt}"}
            ]
        }
        
        response = requests.post(provider['api_url'], headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result['content'][0]['text']
    except Exception as e:
        print(f"[!] Anthropic API error: {e}")
        return None


def call_google_api(provider: dict[str, Any], prompt: str) -> str | None:
    """Call Google Gemini API."""
    try:
        url = f"{provider['api_url']}?key={provider['api_key']}"
        
        data = {
            'contents': [{
                'parts': [{
                    'text': f"{provider.get('instructions', '')}\n\n{prompt}"
                }]
            }],
            'generationConfig': {
                'maxOutputTokens': min(provider.get('max_tokens', 1000000), 8192),
                'temperature': provider.get('temperature', 0.7)
            }
        }
        
        response = requests.post(url, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print(f"[!] Google API error: {e}")
        return None


def call_openrouter_api(provider: dict[str, Any], prompt: str) -> str | None:
    """Call OpenRouter API (OpenAI-compatible)."""
    return call_openai_api(provider, prompt)


def find_tool_executable(command: str) -> str | None:
    """Find tool executable in PATH or Windows installation folders."""
    # First check PATH
    path_exe = shutil.which(command)
    if path_exe:
        return path_exe
    
    # On Windows, check installation folders
    if platform.system() == "Windows":
        install_paths = get_windows_install_paths()
        if command in install_paths:
            for install_path in install_paths[command]:
                if os.path.exists(install_path):
                    return install_path
    
    return None


class Tool:
    def __init__(self, name: str, command: str, description: str, examples: list[str]):
        self.name = name
        self.command = command
        self.description = dedent(description).strip()
        self.examples = examples
        self._executable_path: str | None = None
        self._availability_checked = False

    def is_available(self) -> bool:
        """Check if tool is available and cache the executable path."""
        if not self._availability_checked:
            self._executable_path = find_tool_executable(self.command)
            self._availability_checked = True
        return self._executable_path is not None

    def get_executable_path(self) -> str:
        """Get the full path to the tool executable."""
        if not self._availability_checked:
            self.is_available()
        return self._executable_path or self.command

    def render(self) -> str:
        is_avail = self.is_available()
        if is_avail:
            exe_path = self.get_executable_path()
            if exe_path != self.command:
                status = f"✅ available ({exe_path})"
            else:
                status = "✅ available"
        else:
            status = "⚠️  not found"
        example_lines = "\n".join(f"   - {ex}" for ex in self.examples)
        return dedent(
            f"""
            --- {self.name} ({self.command}) ---
            {self.description}
            Status: {status}
            Sample usage:
            {example_lines}
            """
        ).strip()


TOOLS: list[Tool] = [
    Tool(
        "ExifTool",
        "exiftool",
        """
        Metadata extractor for almost any file format. Great for spotting
        hidden data, timestamps, GPS info, and camera details.
        """,
        [
            "exiftool suspicious.jpg",
            "exiftool -ver",
            "exiftool -a -G1 -s image.png",
        ],
    ),
    Tool(
        "Binwalk",
        "binwalk",
        """
        Firmware and binary analysis tool. Scans files for embedded files,
        signatures, and compressed data.
        """,
        [
            "binwalk firmware.bin",
            "binwalk -e firmware.bin",
            "binwalk -E -M target.img",
        ],
    ),
    Tool(
        "zsteg",
        "zsteg",
        """
        Detects steganographic payloads in PNG/BMP files, focusing on LSB
        encodings. Supports quick brute-force searches.
        """,
        [
            "zsteg secret.png",
            "zsteg -E b1,bgr,msb secret.bmp",
            "zsteg -a suspicious.png",
        ],
    ),
    Tool(
        "Hashcat",
        "hashcat",
        """
        GPU-accelerated password cracker supporting numerous hash formats.
        Requires specifying hash mode and attack strategy.
        """,
        [
            "hashcat -m 0 hashes.txt wordlist.txt",
            "hashcat -I  # list available devices",
            "hashcat -m 1000 hash.txt -a 0 rockyou.txt",
        ],
    ),
    Tool(
        "John the Ripper",
        "john",
        """
        CPU-based password cracker with smart rules and format autodetection.
        """,
        [
            "john hashes.txt",
            "john --wordlist=rockyou.txt hashes.txt",
            "john --show hashes.txt",
        ],
    ),
    Tool(
        "GNU Coreutils (strings/xxd/etc.)",
        "strings",
        """
        Collection of Unix utilities for Windows (strings, xxd, base64, cut,
        sort, etc.). Uses whichever binary you invoke.
        """,
        [
            "strings -n 6 binary.bin",
            "xxd file.bin | head",
            "base64 -d payload.b64 > payload.bin",
        ],
    ),
    Tool(
        "ncat (from Nmap)",
        "ncat",
        """
        Flexible networking swiss-army knife for TCP/UDP sockets, relays,
        and port listeners. Compatible with traditional netcat syntax.
        """,
        [
            "ncat -lvnp 9001",
            "ncat target 80",
            "ncat --ssl target 443",
        ],
    ),
    Tool(
        "curl",
        "curl",
        """
        Command-line data transfer tool supporting HTTP(S), FTP, and more.
        Handy for API probing and quick downloads.
        """,
        [
            "curl https://example.com",
            "curl -I https://target",
            "curl -o dump.bin https://host/file.bin",
        ],
    ),
    Tool(
        "Ghidra",
        "ghidraRun",
        """
        NSA's reverse-engineering suite for binaries and APKs. Launches a GUI
        workspace with disassemblers, decompilers, and scripting support.
        """,
        [
            "ghidraRun",
            "ghidraRun project_name",
            "ghidraRun &  # launch in background on Linux/macOS",
        ],
    ),
    Tool(
        "radare2",
        "radare2",
        """
        Lightweight reversing framework with command-line UI. Includes r2,
        Cutter GUI, and many utilities for static/dynamic analysis.
        """,
        [
            "radare2 binary.bin",
            "radare2 -d ./a.out  # debug mode",
            "radare2 -qc 'aaa; s main; pdf' binary.bin",
        ],
    ),
    Tool(
        "Wireshark",
        "wireshark",
        """
        Packet capture and analysis GUI with dissectors for hundreds of
        protocols. Launch with admin rights to capture live interfaces.
        """,
        [
            "wireshark",
            "wireshark -r capture.pcapng",
            "tshark -r capture.pcap -Y \"http\"",
        ],
    ),
    Tool(
        "Burp Suite Community",
        "burpsuite",
        """
        Web proxy/interceptor for web-app testing. Community edition is GUI
        only; start the listener and browse through the proxy.
        """,
        [
            "burpsuite",
            "burpsuitecommunity",
            "start burpsuite  # Windows launch",
        ],
    ),
    Tool(
        "CyberChef",
        "cyberchef",
        """
        Browser-based Swiss-army knife for encodings, crypto, and data
        manipulation. Desktop build opens a local Electron wrapper.
        """,
        [
            "cyberchef",
            "start cyberchef  # Windows Electron build",
            "python -m webbrowser https://gchq.github.io/CyberChef/",
        ],
    ),
]


def print_menu() -> None:
    print("\n=== CTF Tool Selector ===")
    for idx, tool in enumerate(TOOLS, start=1):
        status = "✅" if tool.is_available() else "⚠️"
        print(f"{idx}. {tool.name:30} {status}")
    print("A. Analyze Challenge File (determine challenge type)")
    print("I. Install CTF Tools")
    print("0. Exit")


def select_tool(choice: str) -> Tool | None:
    choice = choice.strip().upper()
    if choice == 'A':
        return None  # Special case for AI analysis
    if choice == 'I':
        return None  # Special case for installation
    if not choice.isdigit():
        return None
    idx = int(choice)
    if idx == 0:
        raise SystemExit(0)
    if 1 <= idx <= len(TOOLS):
        return TOOLS[idx - 1]
    return None


def install_tools_windows() -> bool:
    """Install CTF tools on Windows using winget and chocolatey."""
    print("\n=== Installing CTF Tools on Windows ===\n")
    
    # Check for winget
    winget_available = shutil.which("winget") is not None
    choco_available = shutil.which("choco") is not None
    
    if not winget_available:
        print("[!] winget not found. Please update Windows 10/11 or install App Installer.")
        return False
    
    if not choco_available:
        print("[!] Chocolatey not found. Installing Chocolatey...")
        try:
            subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command",
                 "Set-ExecutionPolicy Bypass -Scope Process; "
                 "[System.Net.ServicePointManager]::SecurityProtocol = 3072; "
                 "iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"],
                check=True
            )
            choco_available = True
        except subprocess.CalledProcessError:
            print("[!] Failed to install Chocolatey. Some tools may not install.")
    
    tools_to_install = [
        ("ExifTool", "winget", "PhilHarvey.ExifTool", None),
        ("Binwalk", "choco", "binwalk", None),
        ("zsteg", "choco", "zsteg", None),
        ("Hashcat", "winget", "hashcat", None),
        ("John the Ripper", "choco", "john", None),
        ("GNU Coreutils", "winget", "GnuWin32.CoreUtils", None),
        ("Nmap (ncat)", "winget", "nmap", None),
        ("curl", "winget", "curl", None),
        ("Ghidra", "winget", "NSA.Ghidra", None),
        ("radare2", "choco", "radare2", None),
        ("Wireshark", "winget", "WiresharkFoundation.Wireshark", None),
        ("Burp Suite Community", "winget", "PortSwigger.BurpSuiteCommunity", None),
        ("CyberChef", "winget", "GCHQ.CyberChef", None),
    ]
    
    installed_count = 0
    failed_count = 0
    
    for tool_name, package_manager, package_name, _ in tools_to_install:
        print(f"🔹 Installing {tool_name}...", end=" ", flush=True)
        
        if package_manager == "winget" and not winget_available:
            print("⚠️  Skipped (winget not available)")
            failed_count += 1
            continue
        
        if package_manager == "choco" and not choco_available:
            print("⚠️  Skipped (chocolatey not available)")
            failed_count += 1
            continue
        
        try:
            if package_manager == "winget":
                result = subprocess.run(
                    ["winget", "install", package_name, "-e", "--silent"],
                    capture_output=True,
                    timeout=300
                )
            else:  # choco
                result = subprocess.run(
                    ["choco", "install", package_name, "-y"],
                    capture_output=True,
                    timeout=300
                )
            
            if result.returncode == 0:
                print("✅")
                installed_count += 1
            else:
                print("⚠️  Failed")
                failed_count += 1
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
            print("⚠️  Failed")
            failed_count += 1
    
    print(f"\n✅ Installed: {installed_count}")
    if failed_count > 0:
        print(f"⚠️  Failed: {failed_count}")
    
    return installed_count > 0


def install_tools_linux() -> bool:
    """Install CTF tools on Linux using apt/yum/pacman/dnf."""
    print("\n=== Installing CTF Tools on Linux ===\n")
    
    # Detect package manager
    package_manager = None
    install_cmd = None
    
    if shutil.which("apt"):
        package_manager = "apt"
    elif shutil.which("yum"):
        package_manager = "yum"
        install_cmd = ["sudo", "yum", "install", "-y"]
    elif shutil.which("dnf"):
        package_manager = "dnf"
        install_cmd = ["sudo", "dnf", "install", "-y"]
    elif shutil.which("pacman"):
        package_manager = "pacman"
        install_cmd = ["sudo", "pacman", "-S", "--noconfirm"]
    else:
        print("[!] No supported package manager found (apt/yum/dnf/pacman)")
        return False
    
    print(f"Using package manager: {package_manager}\n")
    
    # Map tools to package names for different distros
    tools_map = {
        "apt": [
            ("ExifTool", "libimage-exiftool-perl"),
            ("Binwalk", "binwalk"),
            ("zsteg", "zsteg"),
            ("Hashcat", "hashcat"),
            ("John the Ripper", "john"),
            ("GNU Coreutils", "coreutils"),
            ("Nmap (ncat)", "nmap"),
            ("curl", "curl"),
            ("Ghidra", "ghidra"),
            ("radare2", "radare2"),
            ("Wireshark", "wireshark"),
            ("Burp Suite Community", "burpsuite"),
            ("CyberChef", None),  # May need manual install
        ],
        "yum": [
            ("ExifTool", "perl-Image-ExifTool"),
            ("Binwalk", "binwalk"),
            ("zsteg", "zsteg"),
            ("Hashcat", "hashcat"),
            ("John the Ripper", "john"),
            ("GNU Coreutils", "coreutils"),
            ("Nmap (ncat)", "nmap"),
            ("curl", "curl"),
            ("Ghidra", "ghidra"),
            ("radare2", "radare2"),
            ("Wireshark", "wireshark"),
            ("Burp Suite Community", None),  # May need manual install
            ("CyberChef", None),  # May need manual install
        ],
        "dnf": [
            ("ExifTool", "perl-Image-ExifTool"),
            ("Binwalk", "binwalk"),
            ("zsteg", "zsteg"),
            ("Hashcat", "hashcat"),
            ("John the Ripper", "john"),
            ("GNU Coreutils", "coreutils"),
            ("Nmap (ncat)", "nmap"),
            ("curl", "curl"),
            ("Ghidra", "ghidra"),
            ("radare2", "radare2"),
            ("Wireshark", "wireshark"),
            ("Burp Suite Community", None),
            ("CyberChef", None),
        ],
        "pacman": [
            ("ExifTool", "perl-image-exiftool"),
            ("Binwalk", "binwalk"),
            ("zsteg", "zsteg"),
            ("Hashcat", "hashcat"),
            ("John the Ripper", "john"),
            ("GNU Coreutils", "coreutils"),
            ("Nmap (ncat)", "nmap"),
            ("curl", "curl"),
            ("Ghidra", "ghidra"),
            ("radare2", "radare2"),
            ("Wireshark", "wireshark"),
            ("Burp Suite Community", None),
            ("CyberChef", None),
        ],
    }
    
    tools_to_install = tools_map.get(package_manager, [])
    
    if package_manager == "apt":
        print("Updating package list...")
        try:
            subprocess.run(["sudo", "apt", "update"], check=True, timeout=120)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            print("[!] Failed to update package list")
    
    installed_count = 0
    failed_count = 0
    skipped_count = 0
    
    for tool_name, package_name in tools_to_install:
        if package_name is None:
            print(f"🔹 {tool_name}... ⚠️  Manual installation required")
            skipped_count += 1
            continue
        
        print(f"🔹 Installing {tool_name}...", end=" ", flush=True)
        
        try:
            if package_manager == "apt":
                cmd = ["sudo", "apt", "install", "-y", package_name]
            elif package_manager == "yum":
                cmd = ["sudo", "yum", "install", "-y", package_name]
            elif package_manager == "dnf":
                cmd = ["sudo", "dnf", "install", "-y", package_name]
            else:  # pacman
                cmd = ["sudo", "pacman", "-S", "--noconfirm", package_name]
            
            result = subprocess.run(cmd, capture_output=True, timeout=300)
            
            if result.returncode == 0:
                print("✅")
                installed_count += 1
            else:
                print("⚠️  Failed")
                failed_count += 1
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
            print("⚠️  Failed")
            failed_count += 1
    
    print(f"\n✅ Installed: {installed_count}")
    if failed_count > 0:
        print(f"⚠️  Failed: {failed_count}")
    if skipped_count > 0:
        print(f"⏭️  Skipped (manual install): {skipped_count}")
    
    return installed_count > 0


def install_tools_macos() -> bool:
    """Install CTF tools on macOS using Homebrew."""
    print("\n=== Installing CTF Tools on macOS ===\n")
    
    if not shutil.which("brew"):
        print("[!] Homebrew not found. Installing Homebrew...")
        print("Visit https://brew.sh to install Homebrew first.")
        return False
    
    tools_to_install = [
        ("ExifTool", "exiftool"),
        ("Binwalk", "binwalk"),
        ("zsteg", "zsteg"),
        ("Hashcat", "hashcat"),
        ("John the Ripper", "john"),
        ("GNU Coreutils", "coreutils"),
        ("Nmap (ncat)", "nmap"),
        ("curl", "curl"),
        ("Ghidra", "ghidra"),
        ("radare2", "radare2"),
        ("Wireshark", "wireshark"),
        ("Burp Suite Community", "burp-suite-community"),
        ("CyberChef", "cyberchef"),
    ]
    
    installed_count = 0
    failed_count = 0
    
    for tool_name, package_name in tools_to_install:
        print(f"🔹 Installing {tool_name}...", end=" ", flush=True)
        
        try:
            result = subprocess.run(
                ["brew", "install", package_name],
                capture_output=True,
                timeout=600
            )
            
            if result.returncode == 0:
                print("✅")
                installed_count += 1
            else:
                print("⚠️  Failed")
                failed_count += 1
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
            print("⚠️  Failed")
            failed_count += 1
    
    print(f"\n✅ Installed: {installed_count}")
    if failed_count > 0:
        print(f"⚠️  Failed: {failed_count}")
    
    return installed_count > 0


def install_tools_interactive() -> None:
    """Interactive tool installation based on platform."""
    system = platform.system()
    
    print("\n" + "=" * 60)
    print("CTF Tools Installation")
    print("=" * 60)
    print(f"Detected platform: {system}")
    print("\nThis will install CTF tools using your system's package manager.")
    print("You may be prompted for administrator/sudo password.")
    
    confirm = input("\nContinue? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        return
    
    success = False
    if system == "Windows":
        success = install_tools_windows()
    elif system == "Linux":
        success = install_tools_linux()
    elif system == "Darwin":  # macOS
        success = install_tools_macos()
    else:
        print(f"[!] Unsupported platform: {system}")
        return
    
    if success:
        print("\n✅ Installation completed!")
        print("Some tools may require a terminal restart to be available.")
    else:
        print("\n⚠️  Installation completed with errors.")
        print("Some tools may need manual installation.")


def analyze_file_interactive() -> None:
    """Interactive file analysis."""
    print("\n=== CTF Challenge Analyzer ===")
    print("Drag and drop a file here, or enter the file path:")
    
    file_path = input("File path: ").strip()
    
    # Handle drag-and-drop (remove quotes if present)
    file_path = file_path.strip('"').strip("'").strip()
    
    if not file_path:
        print("Cancelled.")
        return
    
    print(f"\nAnalyzing: {file_path}")
    print("This may take a moment...\n")
    
    provider = get_best_ai_provider()
    
    result = analyze_file_with_ai(file_path, provider)
    
    if result:
        print("=" * 60)
        print("CHALLENGE ANALYSIS RESULT")
        print("=" * 60)
        print(result)
        print("=" * 60)
    else:
        print("[!] Analysis failed. Please check your configuration.")


def run_tool(tool: Tool) -> None:
    if not tool.is_available():
        print(f"[!] {tool.command} is not found. Install it first.")
        print(f"    Run CTF_Toolkit_FullInstaller.bat to install CTF tools.")
        return

    executable = tool.get_executable_path()
    user_args = input(
        f"Enter arguments for `{tool.command}` (leave empty to cancel): "
    ).strip()
    if not user_args:
        print("Cancelled.")
        return

    cmd = [executable, *shlex.split(user_args)]
    print(f"\n$ {' '.join(shlex.quote(part) for part in cmd)}\n")
    try:
        subprocess.run(cmd, check=False)
    except FileNotFoundError:
        print(f"[!] Unable to launch {executable}. Is it installed?")


def main() -> None:
    print(
        dedent(
            """
            CTF Tool Selector with Challenge Analyzer
            ------------------------------------------
            Choose a tool to see quick usage notes. Press 'r' after viewing a tool
            to run it with custom arguments, or Enter to go back to the menu.
            
            Use option 'A' to analyze a challenge file and determine the challenge type.
            You can drag and drop files or paste file paths.
            """
        ).strip()
    )

    while True:
        print_menu()
        choice = input("Select option: ").strip()
        try:
            tool = select_tool(choice)
        except SystemExit:
            print("Goodluck on your CTFs!")
            raise
        
        if choice.upper() == 'A':
            analyze_file_interactive()
            continue
        
        if choice.upper() == 'I':
            install_tools_interactive()
            input("\nPress Enter to continue...")
            continue
        
        if tool is None:
            print("Please enter a valid option.")
            continue

        print()
        print(tool.render())
        action = input("\nType 'r' to run, anything else to return: ").strip().lower()
        if action == "r":
            run_tool(tool)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Bye!")

