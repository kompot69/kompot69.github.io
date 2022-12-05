# Friendly Telegram File Downloader (Uploader) module by @kompot_69

import logging
import time
import os
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
        command = "wget -0 tempfile "+str(args[0])
        await message.edit("<b>Загружаю файл...</b>")
        try:
           os.system(command)
        except ValueError:
           return await message.edit("<b>Не удалось загрузить файл!</b>")
        await message.edit("<b>Выгружаю файл...</b>")
        
        try:
           os.system("rm filename")
        except ValueError:
           await message.client.send_message(message.to_id, "<b>Не удалось удалить временный файл!<\b>")
        await message.client.send_message(message.to_id, "<b>Не удалось удалить временный файл!<\b>")
        await message.edit("<b>Готово!</b> Временный файл удалён.")
