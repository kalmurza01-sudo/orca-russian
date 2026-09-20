#!/usr/bin/env python3
"""Сборка locales/ru.json из батчей work/ru/*.json (плоские key -> строка).
Проверки — те же, что в загрузчике Orca (parsePluginLanguagePackArtifact):
≤ 20 000 записей, глубина ≤ 16, ключи без точек и управляющих символов,
защищённые пути auto.components.settings.plugin* не трогаем, строка ≤ 8192,
плейсхолдеры {{...}} сохранены."""
import json, glob, re, sys, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
en = json.load(open(f'{root}/work/en.json', encoding='utf-8'))
def flat(o, p=''):
    for k, v in o.items():
        q = f'{p}.{k}' if p else k
        if isinstance(v, dict): yield from flat(v, q)
        else: yield q, v
enf = dict(flat(en))
ru = {}
for f in sorted(glob.glob(f'{root}/work/ru/*.json')):
    ru.update(json.load(open(f, encoding='utf-8')))
bad = 0; out = {}
PH = re.compile(r'\{\{[^}]+\}\}')
for k, v in ru.items():
    if k not in enf: print('нет в en:', k); bad += 1; continue
    if re.match(r'auto\.components\.settings\.plugin', k, re.I): print('защищённый путь:', k); bad += 1; continue
    if not isinstance(v, str) or len(v) > 8192: print('плохое значение:', k); bad += 1; continue
    if sorted(PH.findall(enf[k])) != sorted(PH.findall(v)): print('плейсхолдеры:', k, '|', enf[k][:60], '|', v[:60]); bad += 1; continue
    if v == enf[k]: continue  # без изменений — пусть падает в английский
    node = out
    parts = k.split('.')
    for part in parts[:-1]: node = node.setdefault(part, {})
    node[parts[-1]] = v
n = sum(1 for _ in flat(out))
json.dump(out, open(f'{root}/locales/ru.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'ru.json: {n} строк из {len(enf)} ({n*100//len(enf)}%), ошибок: {bad}')
sys.exit(1 if bad else 0)
