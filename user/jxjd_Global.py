from telethon import events
from .. import user
from ..diy.utils import read
import requests

@user.on(events.NewMessage(pattern=r'^jx', outgoing=True))
async def jcmd(event):
    strText = ""
    if event.is_reply:
        reply = await event.get_reply_message()
        strText = reply.text
    else:
        msg_text = event.raw_text.split(' ')
        if isinstance(msg_text, list) and len(msg_text) == 2:
            strText = msg_text[-1]

    if not strText:
        await user.send_message(event.chat_id, '请指定要解析的口令，格式：jx 口令 或对口令直接回复jx')
        return

    data = {"key": strText}
    response = requests.post("http://自建sign地址/jd/jKeyCommand", data=data, headers={"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8;"})
    if response.status_code == 200:
        result = response.json()
        if result["code"] == 200:
            title = result["data"]["title"]
            jump_url = result["data"]["jumpUrl"]
            await user.send_message(event.chat_id, f"{title}\n{jump_url}")
        else:
            await user.send_message(event.chat_id, f"解析出错：{result['data']}")
    else:
        await user.send_message(event.chat_id, "请求出错，HTTP状态码：" + str(response.status_code))
