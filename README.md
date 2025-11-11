# Vannkraftverk Visualizer

En interaktiv webapplikasjon for å utforske og visualisere alle vannkraftverk i Norge basert på data fra NVE (Norges vassdrags- og energidirektorat).

## Funksjoner

### Søk og filtrering
- **Tekstsøk**: Søk etter vannkraftverk etter navn
- **Geografisk filtrering**: Filtrer på fylke og kommune
- **Ytelsesfilter**: Filtrer på minimum og maksimum ytelse (MW)
- **Tidsfilter**: Filtrer på idriftsettelsesår

### Visualisering
- **Oversiktsliste**: Se alle vannkraftverk som matcher søkekriteriene
- **Fargekodet ytelse**:
  - 🟢 Grønn: Store kraftverk (>100 MW)
  - 🟠 Oransje: Mellomstore kraftverk (20-100 MW)
  - 🔵 Blå: Små kraftverk (<20 MW)
- **Detaljvisning**: Klikk på et anlegg for å se fullstendige detaljer
- **Google Maps-integrasjon**: Åpne hvert anlegg direkte i Google Maps

### Data
- **Sanntidsdata**: Henter data direkte fra NVEs offentlige API
- **Omfattende informasjon**:
  - Anleggsnummer og navn
  - Lokasjon (kommune, fylke, koordinater)
  - Tekniske data (ytelse, fallhøyde, produksjon)
  - Status og konsesjonsinformasjon
  - Idriftsettelsesår

## Bruk lokalt

### Enkel bruk
Åpne bare `index.html` i en moderne nettleser. Applikasjonen vil automatisk laste data fra NVE.

### Kjør med lokal webserver (valgfritt)
```bash
# Python 3
python3 -m http.server 8000

# Node.js (med npx)
npx serve

# Åpne deretter http://localhost:8000 i nettleseren
```

## Deploy til Azure

### Azure Static Web Apps

1. **Opprett en Static Web App i Azure Portal**
   ```bash
   az staticwebapp create \
     --name vannkraftverk-visualizer \
     --resource-group <din-resource-group> \
     --source . \
     --location "West Europe" \
     --branch main
   ```

2. **Push til GitHub**
   ```bash
   git init
   git add index.html README.md
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <din-github-repo>
   git push -u origin main
   ```

3. **Koble GitHub til Azure**
   - Gå til Azure Portal → Static Web Apps
   - Koble til GitHub repository
   - Velg branch og mappestruktur
   - Azure vil automatisk deploye

### Azure App Service (alternativ)

1. **Opprett en App Service**
   ```bash
   az webapp up --name vannkraftverk-visualizer \
     --resource-group <din-resource-group> \
     --runtime "NODE:18-lts" \
     --sku FREE
   ```

2. **Deploy filen**
   - Bruk Azure Portal → App Service → Deployment Center
   - Last opp `index.html`

### Azure Blob Storage + Static Website (billigst)

1. **Aktiver static website hosting**
   ```bash
   az storage blob service-properties update \
     --account-name <storage-account> \
     --static-website \
     --index-document index.html
   ```

2. **Last opp filen**
   ```bash
   az storage blob upload \
     --account-name <storage-account> \
     --container-name '$web' \
     --name index.html \
     --file index.html
   ```

## Teknisk informasjon

### API
Applikasjonen bruker NVEs offentlige ArcGIS REST API:
- **Service**: https://nve.geodataonline.no/arcgis/rest/services/Vannkraft1/MapServer
- **Layer**: 0 (Vannkraftverk)
- **Format**: JSON med geometri (WGS84, EPSG:4326)

### Datafelt
- `vannkraftverkNr`: Unikt anleggsnummer
- `vannkraftverkNavn`: Navn på kraftverket
- `kommunenummer`: Kommunenummer
- `kommuneNavn`: Kommunenavn
- `fylke`: Fylke
- `konsesjonStatus`: Status for konsesjon
- `status`: Driftsstatus (D = I drift)
- `idriftsattAar`: År kraftverket ble satt i drift
- `maksYtelse_MW`: Maksimal ytelse i megawatt
- `midlereProduksjon_GWh`: Gjennomsnittlig årlig produksjon i gigawattimer
- `bruttoFallhoyde_m`: Brutto fallhøyde i meter
- `lat`: Breddegrad (latitude)
- `lon`: Lengdegrad (longitude)

### Teknologier
- **Frontend**: Vanilla JavaScript (ingen dependencies)
- **Styling**: CSS3 med moderne features
- **API-kommunikasjon**: Fetch API
- **Kartintegrasjon**: Google Maps URL-skjema

## Prosjektstruktur

```
NVE_Anleggsregister/
├── index.html                      # Hovedapplikasjon
├── README.md                       # Denne filen
├── generate_visualizer.py          # Python-script for offline versjon (valgfri)
└── vannkraftverk-visualizer.html   # Offline versjon med innebygd data (valgfri)
```

## Nettleserkompatibilitet

Applikasjonen fungerer i alle moderne nettlesere:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Opera 76+

## Datakilde og lisens

Data er hentet fra NVEs offentlige API og er underlagt [Norsk lisens for offentlige data (NLOD)](https://data.norge.no/nlod/no).

### NVE Attribution
Data levert av [Norges vassdrags- og energidirektorat (NVE)](https://www.nve.no/)

## Ytterligere ressurser

- [NVE Hjemmeside](https://www.nve.no/)
- [NVE ArcGIS Services](https://nve.geodataonline.no/arcgis/rest/services)
- [NVE Kraftverk Database](https://www.nve.no/energi/energisystem/kraftproduksjon/vannkraft/)

## Utviklet med

Dette prosjektet er utviklet med hjelp fra Claude Code.

## Kontakt

For spørsmål eller problemer, vennligst opprett et issue i prosjektets repository.

---

**Sist oppdatert**: November 2025
