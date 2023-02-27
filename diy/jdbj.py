import requests
from bs4 import BeautifulSoup
from telethon import events
from asyncio import sleep
from .. import jdbot

@jdbot.on(events.NewMessage(pattern=r'^(http|https)://item\.jd\.com/(.*?).html', outgoing=True))
async def jdc(event):
    url = event.text.strip()
    sku = url[url.rfind('/') + 1:url.rfind('.')]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
        'Referer': url
    }
    r = requests.get(f'https://p.3.cn/prices/mgets?skuIds=J_{sku}&pduid=16136464928071471035749', headers=headers)
    price = r.json()[0]['op']
    soup = BeautifulSoup(requests.get(url, headers=headers).text, 'html.parser')
    title = soup.find('div', {'class': 'sku-name'}).text.strip()
    prices = []
    for li in soup.find_all('li', {'class': 'item clearfix'}):
        prices.append((li.find('div', {'class': 'p-time'}).text.strip(), li.find('div', {'class': 'p-price'}).strong.text.strip()))
    msg = f"商品名称：{title}\n当前价格：{price}\n\n历史价格：\n"
    msg += '\n'.join([f"{t[0]}：{t[1]}" for t in prices])
    max_price = max(prices, key=lambda x: float(x[1]))[1]
    min_price = min(prices, key=lambda x: float(x[1]))[1]
    max_time = [t[0] for t in prices if t[1] == max_price]
    min_time = [t[0] for t in prices if t[1] == min_price]
    msg += f"\n\n最高价：{max_price}（{','.join(max_time)}）\n最低价：{min_price}（{','.join(min_time)}）\n\n该消息将在15秒后删除"
    reply_msg = await event.reply(msg)
    await sleep(15)
    await jdbot.delete_messages(chat_id=reply_msg.chat_id, message_ids=reply_msg.id)
