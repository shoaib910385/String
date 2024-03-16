import base64
import struct
import asyncio
import ipaddress
import requests as r

from Hack import bot
from logger import LOGGER
from traceback import format_exc
from env import LOG_GROUP_ID, MUST_JOIN, DISABLED

from telethon import errors, Button
from telethon.events import CallbackQuery
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.sessions.string import _STRUCT_PREFORMAT, CURRENT_VERSION, StringSession
from telethon.errors.rpcerrorlist import UserNotParticipantError, UserIsBlockedError


MENU1 = '''
A - التحقق من المجموعات والقنوات الـتي يملكـها 🕷. 

B - افحـص المعلومات مثـل الرقم والمـعرف والخ... 🕷. 

C - قم بإزاله اعضـاء مـن جـروب 🕷.

D - اذا سجلت دخـول بالرقم تسطيع مـعرفه الـكود 🕷... 

E - انضـم الي قناه او جـروب 🕷. 

F - مـغادره كـل الـقنوات والجـروبات 🕷.

G - الخـروج من جـروب او قـناه 🕷.

H - مـعرفه اذا كان الحساب به تحتقق بـخطوتين ام لا 🕷. 
'''

MENU2 = '''
I - حـذف جيمع الجلسات معاد جلسه التيرمكس 🕷. 

J - حـذف الحسـاب من الـتليجرام 🕷. 

K - غـادر المجموعات والقنوات كلها 🕷. 

L - اذاعه للكـل 🕷. 

M - انهاء جلسه التيرمكس من الحـساب

N - ارسل اي شي الي الجيمع 🕷.

O - مسح شخص من الادمنيه 🕷. 

P - رفع شخص ادمن 🕷. 
'''

BROADCAST_BUTTONS = [[
    Button.inline("Group", data="1"),
    Button.inline("User", data="2"),
], [
    Button.inline("All", data="3"),
]]

BROADCAST_OPTION = {
    b"1": {
        "group": True
    },
    b"2": {
        "user": True
    },
    b"3": {
        "group": True,
        "user": True
    }
}

KEYBOARD1 = [
    [
        Button.inline("A", data="A"),
        Button.inline("B", data="B"),
        Button.inline("C", data="C"),
        Button.inline("D", data="D")
    ],
    [
        Button.inline("E", data="E"),
        Button.inline("F", data="F"),
        Button.inline("G", data="G"),
        Button.inline("H", data="H")
    ],
    [
        Button.inline("Next ⏭️", data="next")
    ]
]

KEYBOARD2 = [
    [
        Button.inline("I", data="I"),
        Button.inline("J", data="J"),
        Button.inline("K", data="K"),
        Button.inline("L", data="L")
    ],
    [
        Button.inline("M", data="M"),
        Button.inline("N", data="N"),
        Button.inline("O", data="O"),
        Button.inline("P", data="P")
    ],
    [
        Button.inline("back ⏮️", data="back")
    ]
]


async def join_checker(e):
    if not MUST_JOIN:
        return True
    chat = await bot.get_entity(MUST_JOIN)
    try:
        await bot(GetParticipantRequest(chat, e.sender_id))
        return True
    except UserNotParticipantError:
        join_chat = f"https://t.me/{chat.username}"
        button = [[
            Button.url(text="Join", url=join_chat),
        ]]

        TEXT = "يـجب الانضـمام اولا الي قناه الـسورس ❄."

        await bot.send_message(e.sender_id, TEXT, buttons=button)

        return False
    except Exception as err:
        LOGGER(__name__).error(err)
        return True


def paste(text):
    link = 'https://spaceb.in/'
    url = 'https://spaceb.in/api/v1/documents'
    payload = {"content": text, "extension": "txt"}
    headers = {
        "Content-Type": "application/json"
    }

    response = r.post(url, json=payload, headers=headers)
    hash = response.json().get('payload').get('id')

    return link + hash


def on_callback(data=None):
    def dec(func):
        async def wrap(e):
            check = await join_checker(e)
            if not check:
                return

            if func.__name__ in DISABLED:
                await e.answer("This function is currently disabled", alert=True)
                return
            try:
                await func(e)
            except errors.common.AlreadyInConversationError:
                pass
            except (asyncio.CancelledError, UserIsBlockedError):
                return
            except Exception as err:
                ERROR_TXT = f'ERROR MESSAGE:- {err}'
                ERROR_TXT += f'\n\nERROR TRACEBACK:- {format_exc()}'
                if LOG_GROUP_ID:
                    try:
                        link = paste(ERROR_TXT)
                        await bot.send_message(LOG_GROUP_ID, link, link_preview=False)
                    except:
                        pass
                else:
                    LOGGER(__name__).error(ERROR_TXT)
                await e.reply('تحدث بعض الأخطاء من جانب الروبوت. يرجى الإبلاغ عن ذلك إلى فريق @Teto_Support,')

        bot.add_event_handler(wrap, CallbackQuery(data=data))

    return dec



# https://github.com/TeamUltroid/Ultroid/blob/main/pyUltroid/startup/connections.py

_PYRO_FORM = {351: ">B?256sI?", 356: ">B?256sQ?", 362: ">BI?256sQ?"}

DC_IPV4 = {
    1: "149.154.175.53",
    2: "149.154.167.51",
    3: "149.154.175.100",
    4: "149.154.167.91",
    5: "91.108.56.130",
}


def validate_session(session):
    # Telethon Session
    if session.startswith(CURRENT_VERSION):
        if len(session.strip()) != 353:
            return False
        return StringSession(session)

    # Pyrogram Session
    elif len(session) in _PYRO_FORM.keys():
        if len(session) in [351, 356]:
            dc_id, _, auth_key, _, _ = struct.unpack(
                _PYRO_FORM[len(session)],
                base64.urlsafe_b64decode(session + "=" *
                                         (-len(session) % 4)),
            )
        else:
            dc_id, _, _, auth_key, _, _ = struct.unpack(
                _PYRO_FORM[len(session)],
                base64.urlsafe_b64decode(session + "=" *
                                         (-len(session) % 4)),
            )
        return StringSession(CURRENT_VERSION + base64.urlsafe_b64encode(
            struct.pack(
                _STRUCT_PREFORMAT.format(4),
                dc_id,
                ipaddress.ip_address(DC_IPV4[dc_id]).packed,
                443,
                auth_key,
            )).decode("ascii"))
    else:
        return False
