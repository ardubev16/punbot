# Prezzo Unico Nazionale BOT

Questo bot manda giornalmente alle 8 la media del PUN e dell'MGP Gas su una
data chat Telegram.

## Setup

Avviare il container docker con le seguenti variabili d'ambiente:

- `TELEGRAM_TOKEN`: token del bot Telegram
- `CHAT_ID`: chat_id della chat su cui mandare i messaggi

Per l'avvio utilizzare il seguente comando:

```bash
docker run --rm -d ghcr.io/ardubev16/punbot:latest \
-v ./data:/data:rw \
-e TELEGRAM_TOKEN=<your-telegram-token> \
-e CHAT_ID=<yuor-chat-id> \
-e TZ=Europe/Rome
```
