# AI Security Case Investigation – Case A

## Om examinationen

Detta repository innehåller min individuella examinationsuppgift för ITSX26, kursvecka 6, vecka 40.

Jag har valt:

**Case A – AI-phishing mot en kommun**

Caset handlar om en kommunal förvaltning som har fått flera välformulerade mejl som ser ut att komma från intern IT-support. Mottagarna uppmanas att logga in via en länk för att behålla åtkomsten till ett internt system. En medarbetare har klickat på länken men uppger att inga uppgifter lämnades. Det finns inga bekräftade uppgifter om intrång och det är inte fastställt att AI har använts för att skapa mejlen.

Analysen använder CIA-triaden och CIS Critical Security Controls v8.1, med fokus på:

- CIS Control 6 – Access Control Management
- CIS Control 8 – Audit Log Management
- CIS Control 14 – Security Awareness and Skills Training

## Repositorystruktur

```text
week40-ai-security-case/
├── README.md
├── ai_usage.md
├── docs/
│   ├── report.md
│   ├── english_security_summary.md
│   └── references.md
└── evidence/
    ├── figures/
    ├── diagrams/
    │   └── event_chain.md
    └── supporting_material/
```

## Innehåll

- `docs/report.md` – huvudrapport och säkerhetsanalys
- `docs/english_security_summary.md` – engelsk säkerhetssammanfattning
- `docs/references.md` – källförteckning
- `ai_usage.md` – redovisning av AI-användning, verifiering och egna korrigeringar
- `evidence/` – relevant tekniskt stödmaterial

## Avgränsning

Analysen utgår endast från de fakta som anges i examinationscaset. Antaganden, hypoteser och information som behöver verifieras markeras separat.

Det finns ingen bekräftad kompromettering av autentiseringsuppgifter, inget bekräftat intrång och inget bevis för att AI har använts för att skapa mejlen.