# Workflow editoriale e SEO per marcododaro.it

Adattamento per Marco Dodaro del 31 ottobre 2026. Applicare insieme a EDITORIAL_GUIDELINES.md prima di creare o aggiornare un articolo. Le istruzioni esplicite di Marco prevalgono sulle convenzioni delle raccolte di riferimento.

## Riferimenti e perimetro

Sono stati consultati i progetti di Agrici Daniel, distribuiti con licenza MIT:

- [claude-seo](https://github.com/AgriciDaniel/claude-seo), revisione `6be93f45064ffbadced572b5d5c95f55fd263af0`: README, seo-content e seo-technical.
- [claude-blog](https://github.com/AgriciDaniel/claude-blog), revisione `354442348815a7f0327077ad89af2c43cf4b4ab4`: README, blog-write, blog-seo-check, blog-cannibalization, research-quality ed editorial pattern review.

Questo documento adatta i metodi alla pubblicazione HTML attraverso GitHub. Non installa Claude Code, non rende disponibili i suoi comandi e non presume che i suoi script siano eseguibili qui. Lo script locale `scripts/blog_preflight.py` è un controllo specifico di questo sito, non il preflight originale di claude-blog.

Per le indicazioni che cambiano nel tempo, verificare la documentazione primaria corrente, in particolare Google Search Central su [contenuti utili](https://developers.google.com/search/docs/fundamentals/creating-helpful-content), [funzioni AI di Search](https://developers.google.com/search/docs/appearance/ai-features) e [Article](https://developers.google.com/search/docs/appearance/structured-data/article). Le raccolte di terzi sono riferimenti operativi, non fonti di regole Google.

## 1. Brief e verifica dell'archivio

Leggere stato di main, istruzioni, HTML pubblicati, articles_meta.json, editorial-log.json, image-manifest.json, blog e sitemap. Controllare la data italiana; una nuova uscita aggiuntiva nella stessa data richiede una richiesta esplicita di Marco.

Prima della ricerca definire e registrare nel registro editoriale:

- pubblico e problema concreto del lettore;
- query principale, intento e risultato utile della lettura;
- area tematica e pagine esistenti con cui collegare l'articolo;
- differenza rispetto alle pagine più vicine per titolo, H1, H2, introduzione, evento, fonti e intento.

Verificare la SERP italiana corrente quando aiuta a capire l'intento. Non inventare volumi, difficoltà o posizioni. La somiglianza delle parole individua candidati da confrontare, non dimostra cannibalizzazione. Non unire articoli, cambiare URL, impostare redirect, canonical verso altre pagine o noindex come conseguenza automatica di tale somiglianza.

## 2. Ricerca e qualità delle prove

Preferire fonti primarie aggiornate. Per ogni affermazione determinante registrare fonte, URL, data di pubblicazione o aggiornamento, periodo misurato e limiti rilevanti. Per documentazione variabile registrare la data di consultazione. Separare data dell'annuncio e data di disponibilità; verificare mercato italiano, requisiti e rollout.

Cercare riscontri indipendenti per affermazioni controverse, valutazioni di efficacia e tendenze. Cinque articoli che riprendono lo stesso comunicato contano come una sola origine. Se un annuncio è disponibile soltanto dal fornitore, attribuirlo chiaramente al fornitore e non presentarlo come conferma indipendente. Nessuna quota artificiale di fonti recenti può sostituire la prova corretta; una fonte storica valida non diventa falsa perché vecchia.

Distinguere fatti verificati, interpretazioni e proposte operative. Un esempio inventato per spiegare un metodo va indicato come ipotetico. Non inventare test svolti, clienti, risultati, citazioni di esperti o esperienze di Marco. Usare case study, recensioni e ricerche originali solo quando esistono prove adeguate. In caso contrario scegliere un'analisi documentata o una guida.

## 3. Scrittura e revisione in due passaggi

Aprire con una risposta utile all'intento, poi sviluppare spiegazioni e implicazioni. Costruire la scaletta sul tema, senza approvazione intermedia nelle uscite già autorizzate. La lunghezza dipende dal contenuto; le 800–1200 parole sono orientative, non un requisito da raggiungere.

La prima revisione riguarda lessico, formule vuote, transizioni ripetute e precisione. La seconda riguarda il testo intero: paragrafi tutti uguali, terne forzate, contrasti senza motivo, H2 costruiti sullo stesso stampo, attenuazioni accumulate, domande retoriche, introduzioni che parlano dell'articolo e chiusure intercambiabili. Correggere il problema nella frase o nel ragionamento, senza sostituire soltanto sinonimi.

Mantenere italiano naturale e professionale, senza prima persona nel corpo. Non aggiungere opinioni o aneddoti per simulare spontaneità. Preservare le qualificazioni necessarie alle prove. Integrare clean-user-facing-text secondo la versione accessibile. Se i singoli script non si leggono tramite skills.read e non sono installati localmente, richiedere il resource /bundle dello stesso package, scaricare il pacchetto in una directory temporanea ed eseguire gli script inclusi. Non divulgare URL firmati del download. Dichiarare eventuali risorse ancora mancanti e non inventare misurazioni. Un rilievo editoriale non certifica paternità del testo o un esito presso rilevatori AI.

Usare H2 descrittivi e H3 solo per vere sottosezioni. FAQ, riassunti, elenchi, tabelle, grafici e video sono facoltativi: inserirli solo se risolvono un bisogno del lettore. Non rendere obbligatori Key Takeaways, quote di domande, statistiche, densità di keyword o intervalli fissi fra immagini. La breve CTA finale conserva il ruolo commerciale già presente nel sito.

## 4. Controlli sul file pronto

Preservare il template grafico corrente, navigazione, footer, font, consenso e singolo script Analytics. Non usare il renderer di claude-blog per sostituire il layout. PDF e copie MDX non sono necessari per un articolo HTML su questo sito.

Conservare URL .html già pubblicati. Per le nuove pagine usare uno slug leggibile coerente con il sito. Titolo e description devono descrivere il contenuto e restare distinti dall'archivio; le lunghezze dei preview sono indicazioni editoriali, non limiti universali di Google.

Controllare un H1, gerarchia, canonical assoluto univoco, robots indicizzabile con max-image-preview:large, contenuto leggibile nell'HTML iniziale, OG e Twitter coerenti, JSON-LD BlogPosting e BreadcrumbList validi. Collegare autore reale e date visibili corrette. datePublished resta originale; dateModified viene aggiornato solo per revisioni sostanziali. Usare ulteriori tipi di schema soltanto se rappresentano contenuto visibile e supportato. Non creare un'Organization o profili social non documentati.

Verificare link interni esistenti e contestuali, anchor comprensibili e almeno un percorso di scoperta verso la nuova pagina. Aggiungere un link entrante da un approfondimento pertinente quando utile. Non imporre 3–10 link o reciprocità fra tutte le pagine. Distinguere citazioni nel testo e riepilogo fonti; la ripetizione dello stesso URL in bibliografia non è automaticamente un errore.

Conservare foto Unsplash gratuite a colori, licenza verificata e unicità cumulativa. Usare la stessa foto per pagina, blog e metadati social/schema. Comparare URL normalizzati, ID, immagini locali e incorporate; eseguire confronto hash/percettivo e ispezione quando applicabile. Il solo confronto degli URL non conclude il controllo visivo. Preservare credito, alt, evidenza panoramica unica e griglia a massimo tre colonne.

Eseguire prima del commit:

```bash
python3 scripts/blog_preflight.py --article nome-articolo.html
```

Il comando controlla file, metadati, collegamenti locali, archivio, sitemap, robots, metadati della foto e coerenza JSON-LD. Restituisce errori bloccanti, avvisi e controlli non automatizzati. Gli avvisi richiedono valutazione; non sono un punteggio SEO. Non certifica validità completa Schema.org, performance, accessibilità, indicizzazione, unicità percettiva o qualità delle fonti.

Controllare la resa a 375, 768 e 1280 pixel con un browser o renderer disponibile, soprattutto dopo modifiche a layout o ritaglio. Registrare viewport ed esito effettivamente verificati. In assenza del renderer segnare il controllo come non eseguito, senza inventare screenshot. Verificare immagini, testo accessibile, menu, breadcrumb, assenza di scorrimento orizzontale e informazioni dell'evidenza visibili presto.

## 5. Pubblicazione, verifica e manutenzione

Scrivere articolo, blog, sitemap, metadati, registro e manifest coerentemente in un commit atomico. Conservare tutte le pagine precedenti, una sola evidenza, vecchia evidenza nella griglia e tutti gli URL nella sitemap. Prima di aggiornare main ricontrollare HEAD, usare expected_sha e force=false.

Dopo il deployment eseguire:

```bash
python3 scripts/blog_preflight.py --article nome-articolo.html --live
```

Il controllo live confronta pagina pubblica e file locale e verifica blog, sitemap, robots e copertina remota se disponibile. Non basta lo status 200: verificare titolo e corpo effettivo. Se la cache o il deployment sono in ritardo, riprovare senza annunciare la pubblicazione come verificata. Comunicare ciò che è davvero riuscito.

Registrare nel log un campo workflow_review con brief, differenziazione dall'archivio, provenienza delle affermazioni principali, revisione editoriale, controllo copertina, controlli locali e pubblici, viewport e controlli saltati con motivo. Non compilare retroattivamente verifiche mai svolte.

Per la manutenzione, segnalare documentazione superata, link rotti e pagine che trattano lo stesso evento. Aggiornare una pagina utile quando soddisfa già l'intento, invece di pubblicare una riscrittura della notizia. Usare dati reali Search Console/Analytics per valutare impressioni, query, click e risultati; se non disponibili dichiararlo. Non introdurre API a pagamento, nuove automazioni, file speciali per AI, nuove integrazioni o modifiche al consenso senza una richiesta pertinente. Nessuna garanzia di ranking, citazione AI o superamento dei rilevatori.
