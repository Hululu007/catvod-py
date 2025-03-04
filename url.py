import json
import os
import requests
import time

# API 地址
api_path = 'https://tvbox.catvod.com/xs/api.json'
#api_path = 'https://raw.githubusercontent.com/celin1286/xiaosa/refs/heads/main/TVBoxOSC/tvbox/api.json'
redirects_path = 'redirects.json'  # 最终输出的 JSON 文件
log_path = 'log.txt'  # 记录完整 API 信息

# 站点映射关系（拼音首字母）
site_mappings = {
    '立播': 'libo',
    '闪电': 'shandian',
    '欧哥': 'ouge',
    '小米': 'xiaomi',
    '多多': 'duoduo',
    '蜡笔': 'labi',  
    '至臻': 'zhizhen',
    '木偶': 'muou',
    '六趣': 'liuqu',
    '虎斑': 'huban',
    '下饭': 'xiafan'
}

print("=== 获取 API 数据 ===")
headers = {'User-Agent': 'okhttp/4.9.0'}
try:
    response = requests.get(api_path, headers=headers, timeout=10)
    response.raise_for_status()
    api_data = response.json()
    print("成功获取 API 数据")
    
    # 记录完整 API 数据到 log.txt
    with open(log_path, 'w', encoding='utf-8') as log_file:
        json.dump(api_data, log_file, ensure_ascii=False, indent=2)
    print(f"✅ API 数据已写入 {log_path}")
    
    sites = api_data.get('sites', [])
    redirects = {}
    
    for site in sites:
        name = site.get('name', '')
        for key, short_key in site_mappings.items():
            if key in name:
                ext = site.get('ext', {})
                site_url = ext.get('site', '') if isinstance(ext, dict) else ext
                if site_url.startswith('http'):
                    redirects[short_key] = site_url  # 直接存储 URL
    
    # 写入 redirects.json
    with open(redirects_path, 'w', encoding='utf-8') as f:
        json.dump(redirects, f, ensure_ascii=False, indent=2)
    print(f"✅ 成功更新 {redirects_path}")
    print(f"📅 更新时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
except Exception as e:
    print(f"❌ 更新过程中出现错误: {str(e)}")
