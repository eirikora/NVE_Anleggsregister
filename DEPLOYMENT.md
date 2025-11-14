# Deployment Guide - Vannkraftsystemer Visualizer

## 🔐 Sikkerhet og Autentisering

**VIKTIG:** Denne applikasjonen er konfigurert med **Azure AD autentisering**.

✅ **Kun NVE-ansatte med Azure AD-konto får tilgang**
✅ **Gratis** - Fungerer på Free tier
✅ **Sikker** - Autentisering på serversiden

**For komplett setup-guide, se:** [`AZURE_AD_SETUP.md`](./AZURE_AD_SETUP.md)

**Rask oversikt:**
1. Opprett Static Web App
2. Opprett Azure AD App Registration
3. Konfigurer Client ID og Secret
4. Deploy applikasjonen

---

## Deployment til Azure Static Web Apps

### Forberedelser

1. **Generer kombinert JSON-fil:**
   ```bash
   python3 convert_to_json.py
   ```

   Dette genererer `vannkraft-data.json` (ca. 7.5 MB) fra alle JSONL-filene.

2. **Filer som skal deployes:**
   ```
   NVE_Anleggsregister/
   ├── index_vann.html              # Hovedapplikasjon
   ├── vannkraft-data.json          # Alle data (kombinert)
   └── staticwebapp.config.json     # Konfigurasjon (inkl. Azure AD)
   ```

   ⚠️ **VIKTIG:** Husk å erstatte `<TENANT_ID>` i `staticwebapp.config.json` med din faktiske Tenant ID!

### Deploy til Azure Static Web Apps

#### Alternativ 1: Via Azure Portal (enklest)

1. Gå til [Azure Portal](https://portal.azure.com)
2. Opprett en ny **Static Web App**
3. Velg **Custom** som deployment source
4. Last opp begge filene via Azure Portal eller Azure CLI

#### Alternativ 2: Via Azure CLI

```bash
# Installer Azure CLI hvis du ikke har det
# brew install azure-cli  # macOS
# choco install azure-cli # Windows

# Login
az login

# Opprett resource group (hvis ny)
az group create --name NVE-Vannkraft-RG --location westeurope

# Opprett static web app
az staticwebapp create \
  --name vannkraft-visualizer \
  --resource-group NVE-Vannkraft-RG \
  --location westeurope

# Deploy filer (erstatt <token> med deployment token fra Azure)
az staticwebapp upload \
  --name vannkraft-visualizer \
  --resource-group NVE-Vannkraft-RG \
  --source-path . \
  --token <deployment-token>
```

#### Alternativ 3: Via GitHub Actions (anbefalt for continuous deployment)

1. Opprett GitHub repository
2. Legg til GitHub Actions workflow (`.github/workflows/azure-static-web-apps.yml`):

```yaml
name: Azure Static Web Apps CI/CD

on:
  push:
    branches:
      - main
  pull_request:
    types: [opened, synchronize, reopened, closed]
    branches:
      - main

jobs:
  build_and_deploy_job:
    runs-on: ubuntu-latest
    name: Build and Deploy Job
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Generate combined JSON
        run: python3 convert_to_json.py

      - name: Build And Deploy
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          action: "upload"
          app_location: "/"
          output_location: ""
```

### Konfigurering

Opprett `staticwebapp.config.json` for Azure-konfigurasjon:

```json
{
  "navigationFallback": {
    "rewrite": "/index_vann.html"
  },
  "mimeTypes": {
    ".json": "application/json"
  },
  "globalHeaders": {
    "Cache-Control": "public, max-age=3600"
  },
  "routes": [
    {
      "route": "/vannkraft-data.json",
      "headers": {
        "Cache-Control": "public, max-age=86400"
      }
    }
  ]
}
```

### Ytelsesoptimalisering

Azure Static Web Apps gjør automatisk:
- ✅ **Gzip/Brotli kompresjon** - Reduserer vannkraft-data.json fra 7.5 MB til ~1-2 MB
- ✅ **CDN caching** - Rask lasting globalt
- ✅ **HTTPS** - Automatisk SSL-sertifikat

### Kostnader

**Azure Static Web Apps - Free Tier:**
- ✅ 100 GB bandwidth per måned (mer enn nok)
- ✅ 0.5 GB storage (vannkraft-data.json er 7.5 MB)
- ✅ Custom domain støtte
- ✅ Automatisk SSL

**Total kostnad:** 0 kr/måned (innenfor free tier)

### Oppdatering av data

Når NVE-dataene oppdateres:

1. Kjør nedlastingsskriptene for å få nye JSONL-filer
2. Kjør `python3 convert_to_json.py` for å regenerere JSON
3. Re-deploy til Azure (via GitHub push eller manuell upload)

### Testing lokalt

Start lokal webserver:
```bash
python3 -m http.server 8000
```

Åpne: http://localhost:8000/index_vann.html

### Feilsøking

**Problem:** `vannkraft-data.json` ikke funnet
**Løsning:** Sjekk at filen ligger i samme mappe som `index_vann.html`

**Problem:** CORS-feil
**Løsning:** Bruk alltid en web server (ikke `file://` protokoll)

**Problem:** Treg lasting
**Løsning:** Sjekk at gzip er aktivert på serveren (Azure gjør dette automatisk)

### Monitorering

Overvåk applikasjonen via:
- Azure Portal → Static Web Apps → Metrics
- Application Insights (valgfritt, krever ekstra setup)

## Alternative deployment-alternativer

### 1. GitHub Pages (gratis)
- Push filene til GitHub repository
- Aktiver GitHub Pages i Settings
- URL: `https://<username>.github.io/<repo-name>/index_vann.html`

### 2. Netlify (gratis)
- Drag & drop filene til Netlify
- Automatisk CDN og HTTPS

### 3. Azure Blob Storage + CDN
- Billigere for store filer
- Krever mer konfigurasjon
