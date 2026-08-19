import re, os, math, html

TEMPLATE = open('template_final.html', encoding='utf-8').read()

MAPPING = [
("01-ai-literacy-aziendale.md", "ai-literacy-in-azienda-cosa-devono-fare-concretamente-le-imprese.html"),
("02-valutare-competenze-ai.md", "come-valutare-le-competenze-ai-dei-dipendenti.html"),
("03-piano-formazione-ai.md", "come-costruire-un-piano-di-formazione-ai-per-unazienda.html"),
("04-digital-twin-avatar-ai.md", "digital-twin-e-avatar-ai-per-la-formazione-aziendale.html"),
("05-etichettatura-contenuti-ai.md", "contenuti-generati-con-lai-quando-devono-essere-dichiarati.html"),
("06-creator-economy-italia.md", "creator-economy-in-italia-come-sta-cambiando-il-mercato.html"),
("07-come-guadagnano-creator.md", "come-guadagnano-i-content-creator.html"),
("08-creator-imprenditore.md", "dal-creator-allimprenditore-come-costruire-un-business-sostenibile.html"),
("09-creator-marketing-b2b.md", "creator-marketing-b2b-perche-interessa-sempre-piu-aziende.html"),
("10-creator-virtuali-influencer-ai.md", "creator-virtuali-e-influencer-ai-opportunita-e-limiti.html"),
("11-come-scegliere-influencer.md", "come-scegliere-un-influencer-per-una-campagna.html"),
("12-microinfluencer-o-macro.md", "microinfluencer-o-grandi-creator-quale-scelta-conviene.html"),
("13-influencer-vs-affiliate.md", "influencer-marketing-e-affiliate-marketing-differenze-e-quando-usare-l.html"),
("14-usage-rights-creator.md", "usage-rights-nei-contratti-con-i-creator.html"),
("15-roi-influencer-marketing.md", "come-misurare-il-roi-dellinfluencer-marketing.html"),
("16-tiktok-shop-italia.md", "tiktok-shop-italia-guida-completa-per-venditori-e-brand.html"),
("17-tiktok-shop-affiliate.md", "tiktok-shop-affiliate-come-funziona-per-brand-e-creator.html"),
("18-prodotti-tiktok-shop.md", "come-scegliere-un-prodotto-da-vendere-su-tiktok-shop.html"),
("19-live-shopping.md", "live-shopping-come-preparare-una-diretta-che-vende.html"),
("20-tiktok-shop-o-amazon.md", "tiktok-shop-o-amazon-quale-piattaforma-conviene.html"),
("21-strategia-social-aziendale.md", "come-costruire-una-strategia-social-per-unazienda.html"),
("22-geo-ai-search.md", "geo-e-ai-search-come-cambia-la-visibilita-dei-brand.html"),
("23-piano-editoriale-dati.md", "come-creare-un-piano-editoriale-basato-sui-dati.html"),
("24-content-repurposing.md", "come-trasformare-un-articolo-in-contenuti-per-tutti-i-social.html"),
("25-strategia-ugc.md", "ugc-e-ugcx-come-utilizzare-i-contenuti-sul-proprio-sito.html"),
("26-vendere-consulenze.md", "come-trasformare-una-competenza-in-un-servizio-di-consulenza.html"),
("27-validare-idea-business.md", "come-validare-unidea-di-business-prima-di-investire.html"),
("28-processo-commerciale-pmi.md", "come-strutturare-un-processo-commerciale-per-una-piccola-impresa.html"),
("29-differenza-startup-pmi.md", "startup-e-pmi-due-modi-diversi-di-costruire-unimpresa.html"),
("30-innovazione-sud-italia.md", "formazione-e-innovazione-come-strumenti-per-lo-sviluppo-del-sud.html"),
]

CATS = [
 ("AI & Formazione", 1, 5),
 ("Creator Economy", 6, 10),
 ("Influencer Marketing", 11, 15),
 ("Social Commerce", 16, 20),
 ("Digital Strategy", 21, 25),
 ("Business & Crescita", 26, 30),
]
def cat_for(n):
    for name, a, b in CATS:
        if a <= n <= b:
            return name
    return "Approfondimenti"

def inline_md(text):
    # links [text](url)
    text = re.sub(r'\[([^\]]+)\]\((https?://[^\)]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', text)
    # bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    return text

def md_to_html(md, slug):
    lines = md.split('\n')
    title = None
    body_parts = []
    sources = {}
    para_buf = []
    def flush_para():
        if para_buf:
            txt = ' '.join(para_buf).strip()
            if txt:
                body_parts.append('    <p>' + inline_md(txt) + '</p>')
            para_buf.clear()

    first_desc_para = None

    for raw in lines:
        line = raw.rstrip()
        if line.startswith('# '):
            title = line[2:].strip()
            continue
        if line.startswith('**[IMMAGINE'):
            continue
        if line.strip() == '---':
            flush_para()
            continue
        if line.startswith('*Articolo correlato'):
            continue
        if line.startswith('### '):
            flush_para()
            body_parts.append('    <h3>' + inline_md(line[4:].strip()) + '</h3>')
            continue
        if line.startswith('## '):
            flush_para()
            body_parts.append('    <h2>' + inline_md(line[3:].strip()) + '</h2>')
            continue
        if line.startswith('- '):
            flush_para()
            item = '      <li>' + inline_md(line[2:].strip()) + '</li>'
            if body_parts and body_parts[-1].startswith('    <ul>'):
                body_parts[-1] = body_parts[-1][:-6] + '\n' + item + '\n    </ul>'
            else:
                body_parts.append('    <ul>\n' + item + '\n    </ul>')
            continue
        if line.strip() == '':
            flush_para()
            continue
        para_buf.append(line.strip())
        # collect links for sources
        for m in re.finditer(r'\[([^\]]+)\]\((https?://[^\)]+)\)', line):
            sources[m.group(2)] = m.group(1)
        if first_desc_para is None:
            first_desc_para = line.strip()

    flush_para()
    body_html = '\n\n'.join(body_parts)

    # description: strip markdown/link syntax from first paragraph, truncate
    desc_raw = first_desc_para or title
    desc_plain = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', desc_raw)
    desc_plain = re.sub(r'\*\*([^*]+)\*\*', r'\1', desc_plain)
    if len(desc_plain) > 160:
        desc_plain = desc_plain[:157].rsplit(' ', 1)[0] + '...'

    word_count = len(re.sub(r'<[^>]+>', '', body_html).split())
    reading_min = max(2, round(word_count / 200))

    sources_html = '\n'.join(
        f'        <li><a href="{url}" target="_blank" rel="noopener">{html.escape(name)}</a></li>'
        for url, name in sources.items()
    ) or '        <li></li>'

    return title, desc_plain, body_html, sources_html, reading_min

OUT_DIR = 'articles_new'
os.makedirs(OUT_DIR, exist_ok=True)

DATE_ISO = '2026-08-19'
META_DATE_HUMAN = '19 agosto 2026'

results = []
for idx, (md_file, out_slug) in enumerate(MAPPING, start=1):
    md_path = os.path.join('/home/claude/uploads_md/articoli', md_file)
    md = open(md_path, encoding='utf-8').read()
    title, desc, body_html, sources_html, reading_min = md_to_html(md, out_slug)
    category = cat_for(idx)
    meta_top = f'{category} &middot; {META_DATE_HUMAN} &middot; {reading_min} minuti'
    cover_style = "background:linear-gradient(135deg, #1a1a1a 0%, #0A0A0A 60%), radial-gradient(circle at 30% 30%, rgba(194,103,46,0.35), transparent 60%);"

    out_html = TEMPLATE
    out_html = out_html.replace('{{TITLE}}', title)
    out_html = out_html.replace('{{DESC}}', desc)
    out_html = out_html.replace('{{DATE_ISO}}', DATE_ISO)
    out_html = out_html.replace('{{META_TOP}}', meta_top)
    out_html = out_html.replace('{{COVER_STYLE}}', cover_style)
    out_html = out_html.replace('{{BODY_HTML}}', body_html)
    out_html = out_html.replace('{{SOURCES_HTML}}', sources_html)

    out_path = os.path.join(OUT_DIR, out_slug)
    open(out_path, 'w', encoding='utf-8').write(out_html)
    results.append((idx, out_slug, title, category, reading_min))

print(f"Generated {len(results)} articles")
for r in results[:5]:
    print(r)
