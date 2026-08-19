import re, os, json, html as htmlmod

SRC = 'gemini-3-7-flash-agenti-ai-aziende.html'
template = open(SRC, encoding='utf-8').read()

# 1. Title
old_title = '<title>Gemini 3.7 Flash ufficiale — agenti AI più economici per le aziende | Marco Dodaro</title>'
assert template.count(old_title) == 1
template = template.replace(old_title, '<title>{{TITLE}} | Marco Dodaro</title>', 1)

# 2. description meta
old_desc = '<meta name="description" content="Google lancia Gemini 3.7 Flash, il modello per agenti AI e coding disponibile tramite Gemini API, Antigravity e Gemini Enterprise.">'
assert template.count(old_desc) == 1
template = template.replace(old_desc, '<meta name="description" content="{{DESC}}">', 1)

# 3. og:title
old_ogtitle = '<meta property="og:title" content="Gemini 3.7 Flash ufficiale — agenti AI più economici per le aziende">'
assert template.count(old_ogtitle) == 1
template = template.replace(old_ogtitle, '<meta property="og:title" content="{{TITLE}}">', 1)

# 4. og:description
old_ogdesc = '<meta property="og:description" content="Google lancia Gemini 3.7 Flash, il modello per agenti AI e coding disponibile tramite Gemini API, Antigravity e Gemini Enterprise.">'
assert template.count(old_ogdesc) == 1
template = template.replace(old_ogdesc, '<meta property="og:description" content="{{DESC}}">', 1)

# 5. published time
old_pub = '<meta property="article:published_time" content="2026-08-17">'
assert template.count(old_pub) == 1
template = template.replace(old_pub, '<meta property="article:published_time" content="{{DATE_ISO}}">', 1)

print("head markers ok, len now", len(template))

# 6. meta-top text
old_metatop = '<div class="article-meta-top">News · 17 agosto 2026 · 3 minuti</div>'
assert template.count(old_metatop) == 1
template = template.replace(old_metatop, '<div class="article-meta-top">{{META_TOP}}</div>', 1)

# 7. h1
old_h1 = '<h1>Gemini 3.7 Flash ufficiale — agenti AI più economici per le aziende</h1>'
assert template.count(old_h1) == 1
template = template.replace(old_h1, '<h1>{{TITLE}}</h1>', 1)

print("meta-top/h1 ok")

open('template_stage1.html', 'w', encoding='utf-8').write(template)
print("saved stage1", len(template))
