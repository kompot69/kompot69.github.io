# Friendly Telegram File Downloader (Uploader) module by @kompot_69

import logging
import time
from datetime import datetime
from io import BytesIO
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.test(args=None)
async def dumptest(conv):
    m = await conv.send_message("test")
    await conv.send_message(".dump", reply_to=m)
    r = await conv.get_response()
    assert r.message.startswith("Message(") and "test" in r.message, r

@loader.test(args="0")
async def logstest(conv):
    r = await conv.get_response()
    assert r.message == "Loading media...", r
    r2 = await conv.get_response()
    assert r2.document, r2

@loader.tds
class DownloadMod(loader.Module):
    """File Downloader by @kompot_69"""
    strings = {"name": "File Downloader",
               "fail": "<b>Не удалось загрузить файл!</b>",
               "bad_link": "<b>Неверная ссылка!</b>",
               "downloading": "<b>Загружаю файл...</b>",
               "uploading": "<b>Выгружаю файл...</b>",
               "filename": "file[{}].txt"}

    @loader.test(resp="Pong")
    @loader.unrestricted
    async def dlfilecmd(self, message):
        """.dlfile <link>
           Download file from link."""
        args = utils.get_args(message)
        if not len(args) == 1:
            return await message.edit("<b>Неверная команда(аргумент)!</b>")
        link = str(args[0])
        
        await message.edit("<b>Загружаю файл...</b>")
        await message.edit("<b>Выгружаю файл...</b>")



    @loader.test(func=logstest)
    async def logscmd(self, message):
        """.logs <level>
           Dumps logs. Loglevels below WARNING may contain personal info."""
        args = utils.get_args(message)
        if not len(args) == 1 and not len(args) == 2:
            args = ["40"]
        try:
            lvl = int(args[0])
        except ValueError:
            # It's not an int. Maybe it's a loglevel
            lvl = getattr(logging, args[0].upper(), None)
        if not isinstance(lvl, int):
            await utils.answer(message, self.strings("bad_loglevel", message))
            return
        if not (lvl >= logging.WARNING or (len(args) == 2 and args[1] == self.strings("logs_force", message))):
            await utils.answer(message,
                               self.strings("logs_unsafe", message).format(lvl=lvl, force=self.strings("logs_force", message)))
            return
        [handler] = logging.getLogger().handlers
        logs = ("\n".join(handler.dumps(lvl))).encode("utf-8")
        if not len(logs) > 0:
            await utils.answer(message, self.strings("no_logs", message).format(lvl))
            return
        logs = BytesIO(logs)
        logs.name = self.strings("logs_filename", message).format(lvl)
        await utils.answer(message, logs)

    @loader.owner
    async def suspendcmd(self, message):
        """.suspend <time>
           Suspends the bot for N seconds"""
        # Blocks asyncio event loop, preventing ANYTHING happening (except multithread ops,
        # but they will be blocked on return).
        try:
            time.sleep(int(utils.get_args_raw(message)))
        except ValueError:
            await utils.answer(message, self.strings("suspend_invalid_time", message))

    async def client_ready(self, client, db):
        self.client = client
