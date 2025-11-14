# Azure AD Autentisering - Setup Guide

## Oversikt

Denne guiden viser hvordan du setter opp Azure Active Directory (Entra ID) autentisering for Vannkraftsystemer Visualizer. Dette gir:

- ✅ **Sikker tilgangskontroll** - Kun NVE-ansatte med Azure AD-konto får tilgang
- ✅ **Single Sign-On (SSO)** - Automatisk innlogging hvis allerede pålogget Azure
- ✅ **Gratis** - Fungerer på Azure Static Web Apps Free tier
- ✅ **Ingen IP-vedlikehold** - Fungerer fra kontor, hjemmekontor, mobil, osv.

---

## Steg 1: Opprett Azure Static Web App

### 1.1 Via Azure Portal

1. Gå til [Azure Portal](https://portal.azure.com)
2. Søk etter **"Static Web Apps"**
3. Klikk **"Create"**
4. Fyll ut:
   - **Subscription:** Velg NVE sitt abonnement
   - **Resource Group:** Opprett ny eller velg eksisterende (f.eks. `NVE-Vannkraft-RG`)
   - **Name:** `vannkraft-visualizer` (eller annet navn)
   - **Region:** `West Europe` (eller nærmeste)
   - **Deployment source:** `Other` (vi laster opp manuelt)
5. Klikk **"Review + Create"** → **"Create"**

### 1.2 Noter ned:
- **Static Web App URL:** `https://vannkraft-visualizer.azurestaticapps.net`
- Du trenger denne senere!

---

## Steg 2: Opprett Azure AD App Registration

### 2.1 Gå til Azure AD

1. I Azure Portal, søk etter **"Azure Active Directory"** eller **"Microsoft Entra ID"**
2. Klikk på **"App registrations"** i venstre meny
3. Klikk **"New registration"**

### 2.2 Konfigurer App Registration

**Name:** `Vannkraft Visualizer`

**Supported account types:**
- Velg: **"Accounts in this organizational directory only (NVE only - Single tenant)"**

**Redirect URI:**
- Type: **Web**
- URI: `https://vannkraft-visualizer.azurestaticapps.net/.auth/login/aad/callback`

  ⚠️ **VIKTIG:** Erstatt `vannkraft-visualizer` med ditt Static Web App navn!

Klikk **"Register"**

### 2.3 Noter ned viktige verdier

Du vil nå se **Overview** siden. Noter ned:

1. **Application (client) ID**
   - Eksempel: `12345678-1234-1234-1234-123456789abc`
   - Vi kaller denne `<CLIENT_ID>`

2. **Directory (tenant) ID**
   - Eksempel: `87654321-4321-4321-4321-cba987654321`
   - Vi kaller denne `<TENANT_ID>`

### 2.4 Opprett Client Secret

1. I venstre meny, klikk **"Certificates & secrets"**
2. Klikk **"New client secret"**
3. Description: `Vannkraft Visualizer Secret`
4. Expires: Velg **24 months** (eller lengre)
5. Klikk **"Add"**
6. **VIKTIG:** Kopier **Value** (secret) NÅ - den vises bare én gang!
   - Eksempel: `abc123def456ghi789...`
   - Vi kaller denne `<CLIENT_SECRET>`

⚠️ **Lagre denne verdien trygt!** Den vises aldri igjen.

---

## Steg 3: Konfigurer Static Web App

### 3.1 Legg til Configuration Settings

1. Gå tilbake til din **Static Web App** i Azure Portal
2. I venstre meny, klikk **"Configuration"**
3. Under **Application settings**, klikk **"Add"**

**Legg til disse to settings:**

**Setting 1:**
- Name: `AZURE_CLIENT_ID`
- Value: `<CLIENT_ID>` (fra steg 2.3)

**Setting 2:**
- Name: `AZURE_CLIENT_SECRET`
- Value: `<CLIENT_SECRET>` (fra steg 2.4)

4. Klikk **"Save"** øverst

### 3.2 Oppdater staticwebapp.config.json

I din `staticwebapp.config.json` fil, erstatt `<TENANT_ID>` med din faktiske Tenant ID:

```json
{
  "auth": {
    "identityProviders": {
      "azureActiveDirectory": {
        "registration": {
          "openIdIssuer": "https://login.microsoftonline.com/<TENANT_ID>/v2.0",
          ...
        }
      }
    }
  }
}
```

**Eksempel:**
```json
"openIdIssuer": "https://login.microsoftonline.com/87654321-4321-4321-4321-cba987654321/v2.0",
```

---

## Steg 4: Deploy Applikasjonen

### 4.1 Forbered filene

```bash
# 1. Generer kombinert JSON
python3 convert_to_json.py

# 2. Sjekk at du har disse filene klare:
ls -lh
# - index_vann.html
# - vannkraft-data.json
# - staticwebapp.config.json (med riktig TENANT_ID)
```

### 4.2 Deploy via Azure Portal

**Alternativ A: Manuell upload**

1. Gå til Static Web App i Azure Portal
2. Klikk **"Overview"** → **"Manage deployment token"**
3. Kopier deployment token
4. Bruk Azure CLI:

```bash
# Install Azure CLI hvis nødvendig
# macOS: brew install azure-cli
# Windows: choco install azure-cli

# Login
az login

# Deploy
az staticwebapp upload \
  --name vannkraft-visualizer \
  --resource-group NVE-Vannkraft-RG \
  --source-path . \
  --token <deployment-token>
```

**Alternativ B: Via GitHub Actions**

Se `DEPLOYMENT.md` for GitHub Actions setup.

---

## Steg 5: Test Autentiseringen

### 5.1 Første test

1. Gå til: `https://vannkraft-visualizer.azurestaticapps.net`
2. Du vil bli redirectet til Microsoft login-side
3. Logg inn med din **NVE Azure AD-bruker** (f.eks. `fornavn.etternavn@nve.no`)
4. Første gang må du godta tilgangen (consent)
5. Du blir redirected tilbake til appen - nå autentisert! ✅

### 5.2 Verifiser innlogging

Åpne DevTools Console og skriv:
```javascript
fetch('/.auth/me')
  .then(r => r.json())
  .then(data => console.log(data));
```

Du skal se informasjon om den påloggede brukeren:
```json
{
  "clientPrincipal": {
    "identityProvider": "aad",
    "userId": "...",
    "userDetails": "fornavn.etternavn@nve.no",
    "userRoles": ["authenticated"]
  }
}
```

### 5.3 Test utlogging

Gå til: `https://vannkraft-visualizer.azurestaticapps.net/.auth/logout`

Du blir logget ut og sendt tilbake til login-siden.

---

## Steg 6: Administrere Tilgang

### 6.1 Begrens til spesifikke brukere (valgfritt)

**Hvis du bare vil gi tilgang til enkelte personer:**

1. Gå til Azure AD → **App registrations** → Din app
2. Klikk **"API permissions"** → **"Add a permission"**
3. Velg **Microsoft Graph** → **Delegated permissions**
4. Legg til: `User.Read`
5. Klikk **"Grant admin consent"**

6. Gå til **"Enterprise applications"** → Finn din app
7. Klikk **"Users and groups"** → **"Add user/group"**
8. Legg til spesifikke brukere eller Azure AD-grupper

### 6.2 Bruk Azure AD-grupper (anbefalt)

**Beste praksis:** Opprett en Azure AD-gruppe kalt "Vannkraft-Visualizer-Users"

1. Azure AD → **"Groups"** → **"New group"**
2. Group type: **Security**
3. Group name: `Vannkraft-Visualizer-Users`
4. Members: Legg til relevante NVE-ansatte
5. Tilbake i **Enterprise application**: Assign denne gruppen

Nå kan du enkelt legge til/fjerne brukere ved å endre gruppe-medlemskap!

---

## Steg 7: Valgfrie forbedringer

### 7.1 Vis innlogget bruker i appen

Legg til i `index_vann.html` (etter `<body>`):

```html
<div id="userInfo" style="position: fixed; top: 10px; right: 10px; background: white; padding: 10px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); z-index: 10000;">
    <span id="userName">Laster...</span> |
    <a href="/.auth/logout" style="color: #0066cc;">Logg ut</a>
</div>

<script>
    // Hent innlogget bruker
    fetch('/.auth/me')
        .then(r => r.json())
        .then(data => {
            if (data.clientPrincipal) {
                document.getElementById('userName').textContent = data.clientPrincipal.userDetails;
            }
        })
        .catch(() => {
            document.getElementById('userName').textContent = 'Ikke innlogget';
        });
</script>
```

### 7.2 Custom login-side (valgfritt)

Opprett `login.html`:

```html
<!DOCTYPE html>
<html lang="no">
<head>
    <meta charset="UTF-8">
    <title>Login - Vannkraftsystemer</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #0066cc 0%, #0099ff 100%);
        }
        .login-box {
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            text-align: center;
            max-width: 400px;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
        }
        p {
            color: #666;
            margin-bottom: 30px;
        }
        .login-btn {
            display: inline-block;
            padding: 12px 30px;
            background: #0066cc;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            transition: background 0.3s;
        }
        .login-btn:hover {
            background: #0052a3;
        }
    </style>
</head>
<body>
    <div class="login-box">
        <h1>Vannkraftsystemer Visualizer</h1>
        <p>Logg inn med din NVE Azure AD-bruker for å få tilgang</p>
        <a href="/.auth/login/aad" class="login-btn">Logg inn med Microsoft</a>
    </div>
</body>
</html>
```

Oppdater `staticwebapp.config.json`:
```json
"responseOverrides": {
  "401": {
    "rewrite": "/login.html"
  }
}
```

---

## Feilsøking

### Problem 1: "Redirect URI mismatch"

**Løsning:**
1. Sjekk at Redirect URI i Azure AD app registration matcher eksakt:
   `https://<din-app>.azurestaticapps.net/.auth/login/aad/callback`
2. Ingen mellomrom eller ekstra tegn

### Problem 2: "AADSTS50011: No reply address"

**Løsning:**
- Legg til Redirect URI i **Authentication** seksjonen (ikke bare Web)
- Velg **ID tokens** under Implicit grant

### Problem 3: "Invalid issuer"

**Løsning:**
- Sjekk at TENANT_ID er riktig i `staticwebapp.config.json`
- Sjekk at `/v2.0` er med i openIdIssuer URL

### Problem 4: Configuration settings ikke tilgjengelig

**Løsning:**
- Vent 2-5 minutter etter å ha lagt til settings
- Restart Static Web App (ikke nødvendig vanligvis)

### Problem 5: Får 401 selv etter innlogging

**Løsning:**
- Sjekk at `staticwebapp.config.json` er deployet
- Sjekk at `allowedRoles: ["authenticated"]` er satt på routes

---

## Sikkerhet og Best Practices

### ✅ DO:
- Bruk Azure AD-grupper for tilgangsstyring
- Sett Client Secret til å utløpe og forny regelmessig
- Overvåk pålogginger via Azure AD logs
- Test logout-funksjonen

### ❌ DON'T:
- Aldri hardkod CLIENT_SECRET i kode
- Ikke del deployment tokens offentlig
- Ikke lag Redirect URIs med wildcards

---

## Kostnader

**Alt er GRATIS:**
- ✅ Azure AD autentisering - Gratis (Basic tier)
- ✅ Azure Static Web Apps - Gratis (Free tier)
- ✅ Ingen ekstra kostnader

---

## Support og Hjelp

**Azure AD dokumentasjon:**
- https://learn.microsoft.com/en-us/azure/static-web-apps/authentication-authorization

**NVE IT-support:**
- Kontakt NVE IT hvis du trenger hjelp med Azure AD-oppsett

**Testing:**
- Test alltid i privat/inkognito modus for å sjekke innlogging fra scratch

---

## Sjekkliste

- [ ] Static Web App opprettet
- [ ] Azure AD App Registration opprettet
- [ ] Client ID og Secret notert ned
- [ ] Redirect URI konfigurert
- [ ] Configuration settings lagt til i Static Web App
- [ ] TENANT_ID oppdatert i staticwebapp.config.json
- [ ] Filer deployet
- [ ] Innlogging testet
- [ ] Utlogging testet
- [ ] Brukere/grupper tildelt (hvis nødvendig)

🎉 **Ferdig!** Appen din er nå sikret med Azure AD autentisering!
