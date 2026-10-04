# AI Security Case Investigation

## Case A – AI-phishing mot en kommun

## 1. Executive Summary

En kommunal förvaltning har fått flera välformulerade mejl som ser ut att komma från intern IT-support. I mejlen uppmanas mottagarna att klicka på en länk och logga in för att behålla åtkomsten till ett internt system. En medarbetare har öppnat länken men uppger att inga uppgifter lämnades. Det finns just nu ingen bekräftad incident och det är inte heller fastställt att AI har använts för att skapa mejlen.

Den största risken är att någon luras att lämna sina inloggningsuppgifter. Om det händer kan en angripare försöka använda kontot för att komma åt kommunens system. Jag bedömer därför konfidentialitet som den viktigaste delen av CIA-triaden i det här caset. Ett kapat konto kan ge åtkomst till information som angriparen inte ska kunna se. Integriteten kan också påverkas om kontot har rätt att ändra information.

Jag bedömer den samlade risken som medelhög. Flera medarbetare har fått mejlen och en person har klickat på länken. Samtidigt finns det inget som bekräftar att några inloggningsuppgifter har lämnats eller att ett konto har tagits över.

De viktigaste åtgärderna är att kontrollera relevanta loggar, säkerställa att MFA och rätt behörighetsnivåer används samt förbättra personalens kunskap om phishing och rapportering. Om loggar eller annan information senare visar att ett konto faktiskt har komprometterats behöver riskbedömningen göras om.

---

## 2. Fakta, antaganden och scope

### 2.1 Givna fakta

Följande uppgifter kommer direkt från caset och behandlas därför som fakta:

- Mejlen har skickats till flera medarbetare.
- Avsändarnamnet liknar intern IT-support.
- Mottagarna uppmanas att logga in via en länk för att behålla åtkomsten till ett internt system.
- En mottagare har öppnat länken.
- Mottagaren uppger att inga uppgifter lämnades.
- Det finns ingen bekräftad information om att inloggningsuppgifter har lämnats.
- Det finns ingen bekräftad incident eller något bekräftat intrång.
- Det är inte fastställt att AI har använts för att skapa mejlen.

Att mejlen är välformulerade är inte i sig ett bevis för att de har skapats med generativ AI.

### 2.2 Antaganden och hypoteser

Det finns flera saker som skulle kunna vara en del av attacken, men som inte är bekräftade i caset:

- Länken kan ha lett till en falsk inloggningssida.
- Syftet kan ha varit att samla in användarnamn, lösenord eller andra autentiseringsuppgifter.
- Om autentiseringsuppgifter hade lämnats skulle de kunna användas för försök till obehörig åtkomst.
- AI kan ha använts för att skriva eller förbättra phishingmejlen.
- Avsändarnamnet kan ha använts för att skapa förtroende genom att efterlikna intern IT-support.

Jag använder alltså inte de här punkterna som fakta i resten av analysen.

### 2.3 Frågor som behöver verifieras

För att ta reda på om något mer än själva phishingförsöket har hänt skulle jag kontrollera:

1. Vilken URL ledde länken till?
2. Vad hände tekniskt när mottagaren öppnade länken?
3. Skickades någon information från användaren eller webbläsaren till webbplatsen?
4. Finns det nya eller avvikande inloggningar på det berörda kontot?
5. Har andra mottagare också klickat på länken?
6. Har någon annan mottagare lämnat inloggningsuppgifter?
7. Används MFA på de berörda systemen?
8. Vilka behörigheter har de berörda användarkontona?
9. Vilken information finns i e-post-, autentiserings-, DNS-, proxy- eller andra säkerhetsloggar?

### 2.4 Scope och avgränsning

Analysen är avgränsad till phishingmejlen, de berörda användarkontona, autentisering, de interna system som skulle kunna påverkas och den tekniska information som kan användas för att undersöka händelsen.

Jag försöker inte identifiera vem som ligger bakom mejlen. Jag försöker inte heller avgöra om AI har använts, eftersom underlaget inte räcker för att dra den slutsatsen.

---

## 3. Tillgångar och händelsekedja

### 3.1 Relevanta tillgångar

#### 1. Användarkonton och autentiseringsuppgifter

Medarbetarnas konton och inloggningsuppgifter är centrala i caset. Om någon får tag i giltiga uppgifter kan de försöka logga in som den riktiga användaren.

#### 2. Kommunens interna system

De interna system som användarna kommer åt är också viktiga tillgångar. Caset säger inte vilka system det gäller eller hur stora behörigheter användarna har, så det går inte att bedöma den exakta konsekvensen utan mer information.

#### 3. Kommunens information

Informationen i de berörda systemen behöver skyddas. Eftersom caset inte säger vilken typ av information systemen innehåller utgår jag inte från att det handlar om någon särskild sorts data.

#### 4. E-postsystemet

E-postsystemet är relevant eftersom phishingmejlen skickas via e-post. Loggar och metadata från e-postsystemet kan också vara användbara när händelsen undersöks.

#### 5. Loggar och säkerhetsevidens

Loggar från autentisering, e-post och andra säkerhetssystem behövs för att kunna se vad som faktiskt har hänt och för att följa upp misstänkt aktivitet.

### 3.2 Händelsekedja

#### Steg 1 – Phishingmejl skickas

Flera medarbetare får välformulerade mejl där avsändarnamnet liknar organisationens interna IT-support.

**Status: Bekräftat i caset.**

#### Steg 2 – Mottagaren uppmanas att agera

Mejlet uppmanar mottagaren att följa en länk och logga in för att behålla åtkomsten till ett internt system.

**Status: Bekräftat i caset.**

#### Steg 3 – En mottagare öppnar länken

En medarbetare klickar på länken. Personen uppger att inga uppgifter lämnades.

**Status: Bekräftat i caset.**

#### Steg 4 – Möjlig insamling av autentiseringsuppgifter

Om länken leder till en falsk inloggningssida skulle nästa steg kunna vara att användaren lämnar sina inloggningsuppgifter.

**Status: Hypotes. Det finns ingen bekräftad information om att detta har hänt.**

#### Steg 5 – Möjlig obehörig åtkomst

Om en angripare hade fått giltiga inloggningsuppgifter skulle dessa kunna användas för att försöka logga in på organisationens system.

**Status: Hypotes. Ingen obehörig åtkomst är bekräftad.**

---

## 4. CIA och enkel riskbedömning

CIA-triaden används för att bedöma hur Confidentiality, Integrity och Availability skulle kunna påverkas.

### 4.1 Confidentiality – konfidentialitet

Om ett konto kapas kan angriparen komma åt samma information som användaren har rätt att läsa.

Det finns inget som visar att detta har hänt i caset, men konsekvensen kan bli stor om ett konto faktiskt tas över.

**Potentiell påverkan: Hög**

### 4.2 Integrity – integritet/riktighet

Om det kapade kontot får ändra information kan angriparen också göra ändringar i den riktiga användarens namn.

Hur allvarligt det blir beror på vilka behörigheter kontot faktiskt har. Det framgår inte av caset.

**Potentiell påverkan: Medel–hög**

### 4.3 Availability – tillgänglighet

Inget i scenariot visar att systemens tillgänglighet har påverkats. Det finns inte heller något som tyder på att målet med mejlen är att orsaka driftstopp.

Ett kapat konto skulle kunna påverka tillgängligheten senare, men det finns inget stöd för att det har hänt här.

**Potentiell påverkan: Låg–medel**

### 4.4 Kvalitativ riskbedömning

Risken jag bedömer är att en användare lämnar sina inloggningsuppgifter genom phishingmejlet och att dessa sedan används för att försöka få obehörig åtkomst till kommunens system.

| Faktor | Bedömning | Motivering |
|---|---|---|
| Sannolikhet | Medel | Flera användare har fått mejlen och en har klickat på länken. Det finns däremot inget som bekräftar att några inloggningsuppgifter har lämnats. |
| Konsekvens | Hög | Om ett konto kapas kan angriparen få åtkomst till information och funktioner som kontot har behörighet till. |
| Samlad risk | Medelhög | Det finns en faktisk exponering och en användare har klickat, men inget intrång är bekräftat. |

Bedömningen gäller utifrån det underlag som finns nu. Om loggar eller annan information visar något annat behöver risken bedömas på nytt.

---

## 5. CIS-mappning

### 5.1 CIS Control 6 – Access Control Management

CIS Control 6 är relevant eftersom ett möjligt mål med phishingförsöket är att få tag i användarnas inloggningsuppgifter.

Om ett lösenord blir stulet kan MFA göra att lösenordet ändå inte räcker för att logga in. Begränsade behörigheter minskar dessutom hur mycket ett kapat konto kan komma åt.

**Åtgärd:**  
Säkerställ att MFA används för relevanta system och att användarnas behörigheter är begränsade efter deras arbetsuppgifter.

**Verifiering:**  
Kontrollera inställningarna i organisationens identitetssystem och testa med ett testkonto. Ett korrekt lösenord utan godkänd MFA ska inte ge åtkomst. Kontrollera även att testkontot bara kommer åt de resurser som det ska ha tillgång till.

### 5.2 CIS Control 8 – Audit Log Management

CIS Control 8 är relevant eftersom organisationen ännu inte vet om phishingförsöket har lett till ett intrång. Loggar behövs därför för att undersöka vad som faktiskt har hänt.

Relevanta loggar kan bland annat visa:

- tidpunkt,
- användarkonto,
- käll-IP,
- lyckade och misslyckade inloggningsförsök,
- MFA-resultat,
- andra säkerhetsrelaterade händelser.

En avvikelse i en logg räcker däremot inte ensam för att säga att ett intrång har skett.

**Åtgärd:**  
Säkerställ att relevanta autentiserings- och säkerhetsloggar samlas in och går att granska.

**Verifiering:**  
Gör ett misslyckat inloggningsförsök med ett testkonto och kontrollera att händelsen registreras med rätt användare, tidpunkt, resultat och relevant information om var försöket kom ifrån.

### 5.3 CIS Control 14 – Security Awareness and Skills Training

CIS Control 14 är relevant eftersom phishing försöker få en människa att utföra en handling. I det här caset har en mottagare redan öppnat länken.

Personalen behöver kunna känna igen varningssignaler och veta vem de ska kontakta när ett IT-meddelande verkar misstänkt.

**Åtgärd:**  
Genomför återkommande utbildning om phishing och social engineering och skapa en tydlig rutin för hur misstänkta IT-meddelanden ska kontrolleras och rapporteras.

**Verifiering:**  
Genomför kontrollerade phishingövningar och följ till exempel klickfrekvens, rapporteringsfrekvens och hur snabbt misstänkta mejl rapporteras.

---

## 6. Prioriterade åtgärder

### Prioritet 1 – Utred händelsen

Granska autentiseringsloggar, e-postloggar och andra relevanta säkerhetsloggar för det berörda kontot och tiden runt händelsen.

Målet är att ta reda på om händelsen stannade vid att användaren öppnade länken eller om det går att hitta någon aktivitet efteråt.

Verifieringen görs genom att dokumentera vilka loggar som kontrollerats, vilken tidsperiod som undersökts, vad man sökt efter och vilka eventuella avvikelser som hittats.

### Prioritet 2 – Säkerställ stark åtkomstkontroll

Säkerställ att relevanta system använder MFA och att användarkonton inte har större behörigheter än vad som behövs för deras arbetsuppgifter.

Målet är att minska skadan om ett lösenord skulle bli stulet.

Det kan verifieras genom ett kontrollerat test där ett korrekt lösenord utan godkänd MFA inte ska ge åtkomst. Behörigheterna kan också kontrolleras mot användarnas faktiska roller.

### Prioritet 3 – Stärk phishingmedvetenhet och rapportering

Genomför återkommande utbildning om phishing och social engineering och ha en tydlig rutin för hur misstänkta IT-meddelanden ska kontrolleras och rapporteras.

Målet är att minska risken för att liknande mejl leder till klick eller att någon lämnar sina inloggningsuppgifter.

Det kan följas upp med kontrollerade phishingövningar där klickfrekvens, rapporteringsfrekvens och tiden det tar innan ett misstänkt mejl rapporteras mäts.

---

## 7. Teknisk koppling

Det här caset går tydligt att koppla till sådant vi tidigare har arbetat med i kursen, framför allt logganalys, identitet och nätverk.

Vid en utredning kan autentiseringsloggar användas för att leta efter aktivitet på det berörda kontot runt tiden då användaren öppnade phishinglänken.

En förenklad autentiseringslogg skulle till exempel kunna innehålla:

    timestamp
    username
    source_ip
    authentication_result
    mfa_result

Om det finns nya inloggningsförsök från en tidigare okänd källa efter klicket är det något som bör undersökas vidare. En ny IP-adress betyder däremot inte automatiskt att någon obehörig har loggat in. Till exempel kan VPN eller en mobilanslutning göra att en vanlig användare får en annan käll-IP.

DNS-, proxy- eller annan nätverksloggning kan också användas för att undersöka om datorn har kommunicerat med den misstänkta domänen.

Jag skulle arbeta enligt följande enkla kedja:

**Händelse → logg/evidens → analys → slutsats**

Poängen är att först titta på vad loggarna faktiskt visar och därefter dra slutsatsen, i stället för att börja med antagandet att ett intrång har skett.

---

## 8. English Security Summary

The municipal organization has received several phishing-like emails impersonating internal IT support. The messages ask employees to follow a link and sign in to retain access to an internal system. One employee is confirmed to have opened the link, but there is no confirmed evidence that credentials were submitted or that an account was compromised.

The main affected assets are user accounts, authentication credentials, internal systems, and organizational information. Confidentiality has the highest potential impact because compromised credentials could enable unauthorized access.

CIS Control 6 – Access Control Management is important because MFA and limited privileges can reduce the impact of compromised passwords. Audit logging and security awareness training are also important for detection and prevention.

The main limitation is the lack of evidence confirming credential theft, unauthorized access, or the use of AI to create the emails.

---

## 9. AI- och källredovisning

AI har använts som ett hjälpmedel för struktur, formulering, språkgranskning och för att kontrollera att de obligatoriska delarna i uppgiften finns med.

AI har inte använts som källa för vad som faktiskt har hänt i caset. Informationen om scenariot kommer från examinationsunderlaget. Information om CIS Controls har kontrollerats mot officiellt material från Center for Internet Security.

En sak som jag har varit noga med är skillnaden mellan fakta och sådant som bara är möjligt. Ett exempel är phishinglänken. Det är rimligt att en sådan länk skulle kunna gå till en falsk inloggningssida, men det står inte i caset att den faktiskt gjorde det. Därför behandlas det som en hypotes.

Samma sak gäller ett möjligt intrång och om AI har använts för att skapa mejlen. Det finns inte tillräckligt med information för att säga att något av detta har hänt.

Fullständig källförteckning finns i `docs/references.md`.

---

## 10. Slutsats

Det som går att fastställa är att flera medarbetare i en kommunal förvaltning har fått phishingliknande mejl som ser ut att komma från intern IT-support. En medarbetare har öppnat länken, men det finns ingen bekräftad information om att några inloggningsuppgifter har lämnats eller att någon obehörig har fått åtkomst till ett konto.

Jag bedömer risken som medelhög med den information som finns nu. Konfidentialitet är den del av CIA-triaden som jag ser som mest kritisk, eftersom ett kapat konto kan ge obehörig åtkomst till information. Integriteten kan också påverkas om kontot får ändra information. Tillgänglighet är mindre central i just det här scenariot eftersom inget tyder på att systemen har blivit otillgängliga.

Det första jag skulle göra är att kontrollera loggar och annan relevant evidens för att se om något hände efter klicket. Därefter är MFA och rätt behörighetsnivåer viktiga för att minska konsekvensen om ett lösenord ändå blir stulet. Utbildning och tydliga rapporteringsrutiner minskar risken för att liknande mejl lyckas i framtiden.

Den största osäkerheten är fortfarande om någon faktiskt har lämnat sina inloggningsuppgifter eller om någon obehörig inloggning har skett. Om det kommer fram ny information om detta behöver riskbedömningen göras om.