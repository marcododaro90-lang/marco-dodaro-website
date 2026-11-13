# Istruzioni editoriali e SEO per marcododaro.it

Repository: marcododaro90-lang/marco-dodaro-website, branch main. La pubblicazione è autorizzata dall'utente.

## Voce e contenuti
Leggere almeno due articoli precedenti pertinenti prima di scrivere. Tono informativo, diretto, professionale e concreto. Niente prima persona nel corpo, opinioni personali attribuite a Marco, esperienze inventate, formule come «la mia lettura», «suggerisco», «propongo», «farei». La breve CTA commerciale può conservare la prima persona. Separare fatti documentati, interpretazioni e proposte operative; presentare esercizi e metodi come esempi applicabili, non risultati dimostrati. Evitare incipit ripetitivi, «Il punto è», trattini incidentali, due punti superflui, periodi che iniziano con «E» e chiusure con domande. La lunghezza dipende dall'utilità, senza minimo artificiale.

## Ricerca e pubblicazione
Verificare fonti primarie aggiornate, date, dati e link. Non duplicare argomenti, notizie, intenti di ricerca o articoli già pubblicati nella data italiana corrente. Usare articles_meta.json, editorial-log.json e tutte le pagine esistenti come stato cumulativo. Conservare URL e datePublished originali; dateModified solo per revisioni sostanziali. Pubblicare articolo, blog, metadati, registro e sitemap in un commit atomico, verificando la testa di main con expected_sha e force=false. Non sovrascrivere modifiche concorrenti.

## Copertine e blog
Conservare le copertine esistenti. Per ogni nuova pubblicazione scegliere una foto gratuita Unsplash, verificata sulla pagina della singola foto sotto Unsplash License; escludere Unsplash+ e premium. Niente immagini generate o copertine tipografiche nuove. Ispezionare la foto e registrare autore e URL, con credito visibile e alt descrittivo. Foto stock sempre indicate come illustrative quando necessario.
Un solo link .blog-featured in cima, sempre il nuovo articolo. Spostare il precedente in evidenza nella .blog-page-grid una sola volta. Mantenere tutti gli articoli pubblicati nell'archivio, inclusi quelli non presenti in articles_meta.json. Nessun duplicato. Massimo tre colonne desktop, una su mobile. Copertina in evidenza a tutta larghezza sopra il testo, ritagliata panoramica con cover, altezza contenuta e punto focale appropriato, mai deformata o contain. Titolo, descrizione e data sotto la foto, visibili presto all'ingresso nel blog. Le regole finali CSS prevalgono sui vecchi stili.

## SEO e verifiche
Definire intento e query principale senza inventare volumi. Titolo specifico, unico H1, introduzione con risposta chiara, H2 descrittivi e meta description unica e completa. Canonical assoluto su https://marcododaro.it/, Open Graph coerente, max-image-preview:large. Collegamenti HTML contestuali a pagine pertinenti e un collegamento entrante da un articolo realmente correlato quando utile. Risolvere i richiami legacy «Articolo correlato: [titolo]» in link effettivi.
BlogPosting e BreadcrumbList JSON-LD coerenti con autore, contenuti, breadcrumb visibili e date reali. Usare immagini HTTP pubbliche, non data URI, nei metadati social e nello schema quando disponibili. Sitemap XML completa con soli URL canonici pubblici, senza template; lastmod solo attendibili. robots.txt deve permettere la scansione e indicare la sitemap. I template pubblici sono noindex: rimuovere obbligatoriamente il noindex dal nuovo articolo generato e sostituire tutti i segnaposto. Non eseguire alla cieca i vecchi generatori che possono rigenerare metadati o layout obsoleti.
Prima del commit controllare JSON/XML, un H1, canonical e description unici, assenza di placeholder e noindex sugli articoli, destinazioni dei link interni, archivio completo e una sola evidenza. Preservare navigazione, analytics, font e componenti. Verificare deployment e contenuti pubblici di articolo, blog, robots e sitemap; distinguere commit riuscito da deployment in attesa. Non inventare test Lighthouse, posizioni o indicizzazione. Search Console serve per verificare query, click, impressioni e stato d'indicizzazione effettivo. Non garantire ranking.


## Fotografie a colori — aggiornamento del 25 ottobre 2026
Per ogni nuovo articolo selezionare una copertina Unsplash gratuita, a colori e visivamente vivace, coerente con il tema e con le immagini già presenti. Verificare sulla pagina della singola fotografia l'uso gratuito sotto Unsplash License; escludere Unsplash+ e premium. Evitare bianco e nero, immagini grigie o desaturate, filtri che eliminano i colori, gradienti e copertine testuali. Ispezionare ogni fotografia e il ritaglio. Usare la stessa fotografia nella pagina articolo, nella scheda del blog, nei metadati Open Graph/Twitter e nei dati strutturati. Aggiungere alt descrittivo, credito al fotografo e link alla pagina della foto; registrare autore, URL originale e licenza nei metadati. Preservare il layout con una sola evidenza panoramica e massimo tre schede per riga. Nessuna nuova scheda senza fotografia.


## Analytics e consenso
Tutte le pagine e i template caricano una sola volta `<script defer src="assets/site-analytics.js?v=20261025-privacy2"></script>`. Il file condiviso gestisce Google Analytics 4 G-MDB7M27NGN e consenso esplicito con accettazione, rifiuto e revoca tramite Preferenze cookie. Conservare questo script anche nei nuovi articoli; non aggiungere lo snippet Google direttamente e non ripristinare il vecchio banner «Ho capito» o la dichiarazione «nessun analytics». Non caricare googletagmanager.com prima del consenso. Conservare il tag google-site-verification sulla homepage. Verificare che non ci siano caricamenti Analytics duplicati.


## Informativa e banner — versione 2026-10-25.2
Preservare la X che rifiuta le statistiche, la scelta Personalizza con categoria statistica non preselezionata per i nuovi visitatori, i pulsanti Accetta/Rifiuta equivalenti e Preferenze cookie nel footer. Conservare il blocco preventivo Analytics, la validità delle scelte per sei mesi, revoca e cancellazione dei cookie. Non dichiarare una conformità legale assoluta né inventare la durata di conservazione impostata nell'account GA4: il dato va verificato nell'account del titolare. Usare la versione dello script presente nei template correnti, anche se vecchie istruzioni riportano una query di versione precedente.


## Unicità delle copertine — 26 ottobre 2026
Ogni articolo deve usare una foto diversa da tutti gli altri articoli. Prima di pubblicare confrontare copertine nell'intero archivio HTML, articles_meta.json, image-manifest.json ed editorial-log.json, normalizzando URL e ID Unsplash senza parametri di ritaglio, qualità o dimensione. La stessa fotografia con ritaglio, URL o nome diverso resta un duplicato. Ispezionare visivamente la candidata e registrare ID, fonte, fotografo e articolo nei metadati. Non dichiarare superato un controllo non eseguito.


## Menu e breadcrumb
Gli stili del menu fisso devono selezionare `body > nav`, mai tutti gli elementi `nav`. Il percorso nell'articolo usa `nav.article-breadcrumb`, statico nel flusso dentro `.article-header .wrap`, con stile discreto e margine inferiore. Verificare che non si sovrapponga alla barra principale su desktop e mobile.


## Revisione finale dei testi — 31 ottobre 2026
Prima di pubblicare applicare la skill clean-user-facing-text alla prosa visibile, preservando codice, URL, citazioni, dati e requisiti SEO. Leggere la versione corrente della skill e seguirne misurazione iniziale, revisione condizionata e pulizia Unicode. Non inventare punteggi o dichiarare eseguiti script non accessibili; registrare il limite e distinguere eventuali controlli locali alternativi. Conservare il tono informativo e professionale, senza prima persona nel corpo o esperienze inventate. La produzione ordinaria punta a cinque articoli originali per data italiana. Per conteggio, fonti e posizionamento seguire il capitolo «Cinque articoli al giorno e modello SEO» di BLOG_WORKFLOW.md.


## Scrittura meno schematica — richiesta del 31 ottobre 2026
Eliminare formule generiche, transizioni che annunciano il discorso e ripetizioni di «può», «permette», «è utile», «un possibile». Non sostituirle con sinonimi ripetuti. Variare la costruzione dei periodi in base al contenuto, accorpare sezioni frammentate e sviluppare esempi concreti già documentati o dichiaratamente ipotetici. Evitare terne forzate, conclusioni intercambiabili e paragrafi costruiti tutti sullo stesso schema. Mantenere H2 utili alla lettura e alla SEO senza trasformare ogni passaggio in una mini-sezione. Conservare fatti, fonti, qualificazioni necessarie e tono professionale; non aggiungere prima persona o esperienze inventate. Valutare la qualità editoriale senza promettere esiti presso rilevatori AI.


## Metodo integrato claude-seo e claude-blog — 31 ottobre 2026
Leggere e applicare BLOG_WORKFLOW.md per brief, ricerca, controllo dell’intento e delle sovrapposizioni, revisione editoriale in due passaggi e verifica tecnica. Eseguire scripts/blog_preflight.py prima del commit e con --live dopo il deployment, correggendo gli errori e registrando separatamente verifiche manuali e limiti. Si tratta dell’adattamento specifico per marcododaro.it, non dell’installazione dei plugin Claude Code. Le preferenze di Marco, gli URL .html, il layout, le copertine Unsplash uniche e il consenso prevalgono sulle convenzioni generiche delle raccolte. Non imporre box, FAQ, PDF, quote di link, soglie di parole o punteggi SEO inventati.


## Scoperta dei temi da Geekout — 31 ottobre 2026
Consultare l'archivio https://geekout.mattnavarra.com/archives, indicato da Marco, per diversificare piattaforme e argomenti delle prossime uscite. Applicare la sezione Geekout di BLOG_WORKFLOW.md: confronto con le pubblicazioni recenti, rilevanza per il pubblico italiano, verifica sulle fonti primarie e attribuzione del contributo editoriale quando usato. Non limitarsi ad AI e TikTok Shop e non riscrivere notizie già pubblicate. Registrare la provenienza dello spunto quando pertinente.


## Home, Insights & risorse — richiesta del 13 novembre 2026
A ogni nuova pubblicazione, manuale o automatica, aggiornare anche la sezione `#blog` di `index.html` nello stesso commit atomico di articolo, blog, sitemap, metadati, manifest e registro. La home mostra i tre articoli più recenti nello stesso ordine del blog: il primo in `.blog-card-featured`, i due successivi in `.blog-side` come `.blog-card-small`. In pubblicazioni multiple selezionare le ultime tre uscite del batch, usando l’ordine effettivo di pubblicazione anche a parità di data. Nessun URL duplicato nella sezione.
Usare titoli, categoria, data, tempo di lettura, descrizione della scheda principale e fotografia coerenti con `articles_meta.json` e con le pagine pubblicate. Riutilizzare per l’anteprima la fotografia già verificata del relativo articolo, con alt accessibile, colore e punto focale coerenti. Preservare struttura grafica e responsive, link «Mostra tutti», navigazione, footer, verifica Search Console e singolo script Analytics con consenso. Non eliminare le vecchie pagine dall’archivio. Aggiornare lastmod della home nella sitemap quando cambia il contenuto.
Prima del commit verificare tre URL unici, ordine uguale ai primi tre del blog, titoli e copertine corrispondenti e destinazioni esistenti. Dopo il deployment aprire anche la home pubblica e confrontare HTML e contenuto della sezione con il file pubblicato; lo status HTTP 200 da solo non basta. Registrare esito o limite nel workflow_review insieme alle altre verifiche.


## Reddit come fonte di spunti — richiesta del 13 novembre 2026
Consultare anche discussioni Reddit pertinenti per individuare domande, problemi pratici e temi emergenti. Verificare data, contesto e URL del thread. Prima di trasformare lo spunto in un articolo cercare altre fonti online, privilegiando documentazione, annunci e ricerche primarie, e riscontri indipendenti quando necessari. Un commento descrive un’esperienza o un’opinione, non dimostra un dato generale, un risultato economico o l’efficacia di un servizio. Non presentare rilanci dello stesso thread come conferme indipendenti. Registrare provenienza dello spunto, fonti di verifica e limiti; se mancano riscontri, mantenere la qualificazione o scegliere un altro tema. Non contattare utenti né pubblicare su Reddit.
