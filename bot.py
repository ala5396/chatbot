import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from tracker import get_prices, get_volume

telegram_bot_token = ""
updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    chat_id = update.effective_chat.id
    message = ""

    crypto_data = get_prices()
    for i in crypto_data:
        coin = crypto_data[i]['coin']
        price = crypto_data[i]['price']
        change_day = crypto_data[i]['change_day']
        change_hour = crypto_data[i]['change_hour']
        message += f"Coin: {coin}\n💰Price: ${price:,.2f}\n📉Hour Change: {change_hour:.3f}%\n📉Day Change: {change_day:.3f}%\n\n"

    context.bot.send_message(chat_id=chat_id, text=message)


def CrypoPrices(update, context):
    chat_id = update.effective_chat.id
    prices = update.effective_message.text.split()[1].upper()

    message = ""
    crypto_data = get_prices()
    if prices in crypto_data:
        coin = crypto_data[prices]['coin']
        price = crypto_data[prices]['price']
        change_day = crypto_data[prices]['change_day']
        change_hour = crypto_data[prices]['change_hour']
        message += f"Coin: {coin}\n💰Price: ${price:,.2f}\n📉Hour Change: {change_hour:.3f}%\n📉Day Change: {change_day:.3f}%\n\n"

    context.bot.send_message(chat_id=chat_id, text=message)


def CryptoVolume(update, context):
    chat_id = update.effective_chat.id

    list_messeage = update.effective_message.text.split()
    mint = int(list_messeage[2].strip())
    coin1 = list_messeage[1].upper().strip()
    coin2 = 'USD'
    if '/' in coin1:
        c = coin1.split('/')
        coin1 = c[0]
        coin2 = c[1]

    message = ""

    data = get_volume(mint, coin1, coin2)

    price = data['price']
    vol = data['vol']
    time = data['time']
    lm = data["LM"]
    p_vol = data['vol_p']
    p_price = data['price_p']
    message += f"{lm} - {coin1}/{coin2} | {coin1}\nVol. changed by \
    {time:,} {coin2} since {mint} min\n📊Vol: {vol:,} {coin2} ({p_vol:.2f}%)\n💰Price: {price:,} {coin2} ({p_price:.2f}%)\n\n"

    context.bot.send_message(chat_id=chat_id, text=message)


dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("p", CrypoPrices))
dispatcher.add_handler(CommandHandler("vol", CryptoVolume))
updater.start_polling()
