# Vannkraftsystemer Visualizer - NVE

Interaktiv webapplikasjon for visualisering av norske vannkraftsystemer fra NVE (Norges vassdrags- og energidirektorat).

## 🎯 Funksjoner

- **Søk og filter** - Søk etter kraftverk, dammer, magasiner med avanserte filtre
- **Interaktiv graf** - Visualiser hierarkiske relasjoner mellom komponenter
- **Detaljert informasjon** - Se alle tekniske detaljer for hvert objekt
- **Relaterte objekter** - Utforsk forbindelser mellom vannkraftsystemer
- **Azure AD autentisering** - Sikker tilgang kun for NVE-ansatte

## 📁 Prosjektstruktur

```
NVE_Anleggsregister/
├── index_vann.html              # Hovedapplikasjon (single-file)
├── vannkraft-data.json          # Kombinert datafil for deployment
├── staticwebapp.config.json     # Azure konfigurasjon (inkl. Azure AD)
│
├── convert_to_json.py           # Script for å generere vannkraft-data.json
│
├── CLAUDE.md                    # Teknisk dokumentasjon
├── DEPLOYMENT.md                # Deployment guide
├── AZURE_AD_SETUP.md            # Azure AD setup guide (steg-for-steg)
└── README.md                    # Denne filen
```

## 🚀 Kom i gang

### Lokal utvikling

1. **Generer datafil:**
   ```bash
   python3 convert_to_json.py
   ```

2. **Start lokal webserver:**
   ```bash
   python3 -m http.server 8000
   ```

3. **Åpne i nettleser:**
   ```
   http://localhost:8000/index_vann.html
   ```

### Deployment til Azure

**Se detaljerte instruksjoner:**
- 📘 [`DEPLOYMENT.md`](./DEPLOYMENT.md) - Generell deployment guide
- 🔐 [`AZURE_AD_SETUP.md`](./AZURE_AD_SETUP.md) - Azure AD autentisering setup

**Rask oversikt:**
1. Opprett Azure Static Web App
2. Konfigurer Azure AD autentisering
3. Deploy `index_vann.html`, `vannkraft-data.json`, og `staticwebapp.config.json`

## 🔐 Sikkerhet

Applikasjonen er sikret med **Azure Active Directory (Entra ID) autentisering**:

- ✅ Kun NVE-ansatte med Azure AD-konto får tilgang
- ✅ Single Sign-On (SSO)
- ✅ Gratis på Azure Static Web Apps Free tier
- ✅ Fungerer fra kontor, hjemmekontor, mobil

## 📊 Data

**Kilde:** NVE (Norges vassdrags- og energidirektorat)

**Datatyper:**
- **Vannkraftverk** - 1,871 anlegg
- **Dammer** - 5,005 anlegg
- **Magasiner** - 2,511 anlegg
- **Vannveier** - 4,441 anlegg
- **Inntakspunkt** - 3,416 anlegg
- **Utløpspunkt** - 1,615 anlegg

**Oppdatering:**
Kjør nedlastingsskriptene i `../NVE_DATA/` for å hente ferske data fra NVE.

## 🛠️ Teknologi

- **Frontend:** Vanilla JavaScript (ingen dependencies)
- **Graf:** vis.js Network
- **Hosting:** Azure Static Web Apps
- **Autentisering:** Azure Active Directory
- **Data:** JSON (gzip komprimert ved serving)

## 📖 Dokumentasjon

### For utviklere
- [`CLAUDE.md`](./CLAUDE.md) - Komplett teknisk dokumentasjon
  - Arkitektur og layout
  - Graf hierarki og logikk
  - Funksjoner og dataflyt
  - Dam-Magasin relasjoner

### For deployment
- [`DEPLOYMENT.md`](./DEPLOYMENT.md) - Deployment alternativer og konfigurasjon
- [`AZURE_AD_SETUP.md`](./AZURE_AD_SETUP.md) - Steg-for-steg Azure AD setup

## 🎨 Funksjoner i detalj

### Hierarkisk graf
```
Level 0: Kraftverk (topp)
         ↓
Level 1: Dam, Vannvei, Inntakspunkt, Utløpspunkt
         ↓ (fra Dam)
Level 2: Magasin (når de tilhører en Dam)
```

### Søk og filtrering
- Søk etter navn
- Filter på type (kraftverk, dam, magasin, osv.)
- Filter på kommune
- Filter på vassdragsnummer

### Interaksjon
- Klikk på resultat → Vis i graf og detaljer
- Klikk på node i graf → Vis detaljer
- Klikk på relatert objekt → Naviger til det objektet

## 💰 Kostnader

**Azure Static Web Apps Free tier:**
- ✅ 100 GB bandwidth/måned (mer enn nok)
- ✅ 0.5 GB storage (vannkraft-data.json = 7.5 MB)
- ✅ Azure AD autentisering inkludert
- ✅ Automatisk SSL og CDN

**Total kostnad:** 0 kr/måned 🎉

## 🔄 Oppdatering av data

Når NVE-dataene oppdateres:

```bash
# 1. Hent nye data
cd ../NVE_DATA
python3 lastned_nve_vannkraftverk.py
python3 lastned_nve_dammer.py
# ... (kjør alle nedlastingsskriptene)

# 2. Generer ny JSON
cd ../NVE_Anleggsregister
python3 convert_to_json.py

# 3. Deploy
az staticwebapp upload \
  --name vannkraft-visualizer \
  --resource-group NVE-Vannkraft-RG \
  --source-path . \
  --token <deployment-token>
```

## 🐛 Feilsøking

### Graf viser ikke alle objekter
- Sjekk at `findDirectRelations()` returnerer riktig data
- Åpne DevTools Console og sjekk for feil

### Azure AD login fungerer ikke
- Sjekk at Redirect URI er korrekt konfigurert
- Verifiser at `<TENANT_ID>` er riktig i `staticwebapp.config.json`
- Se [`AZURE_AD_SETUP.md`](./AZURE_AD_SETUP.md) for troubleshooting

### Data laster ikke
- Sjekk at `vannkraft-data.json` ligger i samme mappe som HTML
- Sjekk nettverkstrafikk i DevTools → Network
- Verifiser at CORS ikke blokkerer (bruk webserver, ikke `file://`)

## 📝 Lisens

Data fra NVE - se [NVE sine vilkår](https://www.nve.no).

## 👥 Kontakt

**NVE IT-support** for spørsmål om Azure AD eller deployment.

---

**Laget med ❤️ for NVE**
