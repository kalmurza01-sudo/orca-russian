#!/usr/bin/env python3
"""Выгрузка английских строк для перевода: export.py <префикс-ключа>... > файл.json"""
import json, sys, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
en = json.load(open(f'{root}/work/en.json', encoding='utf-8'))
def flat(o, p=''):
    for k, v in o.items():
        q = f'{p}.{k}' if p else k
        if isinstance(v, dict): yield from flat(v, q)
        else: yield q, v
sel = {k: v for k, v in flat(en) if any(k.startswith(pfx) for pfx in sys.argv[1:]) and isinstance(v, str)}
json.dump(sel, sys.stdout, ensure_ascii=False, indent=0)
