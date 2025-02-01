
import asyncio
import json
from telegram import constants
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, ContextTypes, filters
from telegram import Update
import requests
import json

from new_rec_manager import new_rec_manager

ngw_host = 'https://blacksea-monitoring.nextgis.com'
auth = None

NG_TEST = False

layer_match = {'oil':60, 'bird':100, "dead":147}

with open("__token_map_to_telegram_bot.txt", "r") as f:
    TELEGRAM_BOT_TOKEN = f.read()

with open("__token_for_map.txt", "r") as f:
    u = f.readline()[:-1]
    p = f.readline()
    auth = (u, p)


# bs_monitoring_map_to_tg_bot
forward_group = -1002335708322 # Анапа. Мониторинг координат

def get_records():
    get_url = ngw_host + '/api/resource/' + str(100) +'/geojson'
    #print(get_url)
    response = requests.get(get_url, auth=auth)
    #print(f"DATA: {json.dumps(response.json(), indent = 4)}")
    response = response.json()
    return response


message_template_photo = """\
[#{id}] {dt_auto} Мск
{comment}
{lat}, {lon}
<a href='https://seagull.nextgis.dev/?zoom=15&center={lon}_{lat}&select=100-{id}&layers=114%2C230%2C101&s%5B101%5D=0%2C1%2C2'>Объхект</a> и <a href='https://blacksea-monitoring.nextgis.com/resource/197/display?panel=identify'>таблица объектов</a>.

Взяли в работу – ставьте ❤️
"""

def prepare_records(records):
    ret = []
    for r in records:
        if r["properties"]["status_photo"] is None:
            continue
        message = message_template_photo
        m = message.format(id = r["id"], comment = r["properties"]["comment"],
                                dt_auto = ":".join(r["properties"]["dt_auto"].split(":")[:1]),
                                lat = r["properties"]["lat"],
                                lon = r["properties"]["lon"],
                                status_us = r["properties"]["status_us"],
                                )
        ret.append(m)
    return ret

async def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    new_rec_manager.init()
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    await application.initialize()
    await application.start()
    print("[OK] Bot enabled")
    while True:
        records = get_records()
        rec_list = new_rec_manager.get_new_features(records)
        prepared_rec_list = prepare_records(rec_list)
        print(f"Scanned. Found {len(prepared_rec_list)} new. Forwarding..")
        for r in prepared_rec_list:
            await application.bot.send_message(forward_group, r, parse_mode=constants.ParseMode.HTML)
            new_rec_manager.update_current_record_id()
            await asyncio.sleep(1) 
        await asyncio.sleep(10)        
    await application.updater.stop()
    print("[OK] Bot disabled")

    await application.shutdown()

if __name__ == "__main__":
    while True:
        asyncio.run(main())
    


