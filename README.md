# PandeMiao
Gotta kill 'em all

Status (CI): 
[![Kitto linter](https://github.com/rage-against-the-data/PandeMiao/workflows/kitto%20linter/badge.svg)](https://github.com/rage-against-the-data/PandeMiao/actions?workflow=kitto_linter)

## How-to
### Come configurarlo
1. Crea un bot su Telegram
2. Inserisci nella variabile `TELEGRAM_API_TOKEN` all'interno di `.env` il token che ti ha dato FatherBot

### Come eseguirlo
1. Esegui `pip install -r requirements.txt`
2. Esegui `. .env`
3. Metti il bot in ascolto: `python bot/listener.py`

### Come eseguirlo con docker-compose
1. Esegui `docker-compose build`
2. Esegui `docker-compose up`

## Altre informazioni
Il logo del bot si trova nella repo https://github.com/rage-against-the-data/logo ed è distribuito con Licenza Creative Commons Attribuzione - Non opere derivate 4.0 Internazionale.
