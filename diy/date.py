import datetime
import locale
import asyncio
from telethon import events
from .. import user

@user.on(events.NewMessage(pattern=r'^date', outgoing=True))
async def show_date(event):
    # 设置本地化参数为中文
    locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
    # 获取当前时间
    now = datetime.datetime.now()
    # 格式化时间字符串
    date_str = now.strftime("%Y年%m月%d日 %A %H:%M:%S")
    # 发送时间字符串，并提示5秒后自动删除
    msg = await event.edit(f"当前时间：{date_str}\n\n此消息将在5秒后自动删除")
    await asyncio.sleep(5)
    await msg.delete()
    await event.delete()
