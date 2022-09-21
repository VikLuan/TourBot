# Progetto TourBot
## Documentazione tecnica

### Descrizione dell'applicazione
#### L'applicazione è composta da più agenti:
- un chatbot __Telegram__ che si interfaccia all'utente per operazioni di input e output
- un agente creato sulla piattaforma __Dialogflow__ per facilitare il ___natural language understanding___ e integrare un'interfaccia utente conversazionale

### Software e librerie usate

 Il __Webhook Service__ costruito in __Python__ è composto da funzioni di scraping della libreria __BeautifulSoup__ che estraggono dati da pagine ___html___ e da funzioni che sfruttano l'___API di Google Maps Platform___ e l'___API di Wikipedia___ per garantire determinati servizi offerti dal chatbot<br />
 
 Il programma utilizza __Ngrok__ che è un ___reverse proxy server cross-platform___ che permette di creare un *tunnel* fra il computer ed internet per un qualsiasi servizio ___http___. In questo modo possiamo esporre un server locale alla rete in sicurezza.
 Questo software permette lo scambio messaggi che avviene tramite file di formato *Json* tra il codice in *Python* e *Dialogflow*<br />

 Il framework __Flask__ è stato utilizzato per sviluppare l'applicazioni Web in linguaggio *Python*

Il bot si può trovare su *telegram* sotto il nome ___@t0ur1st_bot___
