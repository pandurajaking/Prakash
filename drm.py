# -*- coding: utf-8 -*-

from __future__ import annotations
from abc import ABC, abstractmethod

import pytz
import datetime
import os, argparse
import asyncio, shlex
from os.path import join
from aiofiles.os import remove
from aiohttp import ClientSession
from typing import  Union, List
from logging import getLogger, FileHandler, StreamHandler, INFO, basicConfig

__version__ = "1.0"
__author__ = "https://t.me/hiddenextractorbot"
__license__ = "MIT"
__copyright__ = "Copyright 2024"


basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[FileHandler('logs.txt', encoding='utf-8'),
              StreamHandler()],
    level=INFO)

LOGGER = getLogger("drm")

os.makedirs("Videos/", exist_ok=True)

def print_ascii_art():
    text = '\033[92m'"""
    ____  ____  __  ___   ____                      __                __
   / __ \/ __ \/  |/  /  / __ \____ _      ______  / /___  ____ _____/ /
  / / / / /_/ / /|_/ /  / / / / __ \ | /| / / __ \/ / __ \/ __ `/ __  / 
 / /_/ / _, _/ /  / /  / /_/ / /_/ / |/ |/ / / / / / /_/ / /_/ / /_/ /  
/_____/_/ |_/_/  /_/  /_____/\____/|__/|__/_/ /_/_/\____/\__,_/\__,_/   
                                                                           
    """'\033[0m''\033[33m'f'v{__version__} by {__author__}, {__license__} @{__copyright__}\n''\033[0m'
    print(text)

class SERVICE(ABC):

    def __init__(self):
        self._remoteapi = "https://app.magmail.eu.org/get_keys"

    @staticmethod
    def c_name(name: str) -> str:
        for i in ["/", ":", "{", "}", "|"]:
            name = name.replace(i, "_")
        return name

    def get_date(self) -> str:
        tz = pytz.timezone('Asia/Kolkata')
        ct = datetime.datetime.now(tz)
        return ct.strftime("%d %b %Y - %I:%M%p")

    async def get_keys(self):
        async with ClientSession(headers={"user-agent": "okhttp"}) as session:
            async with session.post(self._remoteapi,
                                    json={"link": self.mpd_link}) as resp:
                if resp.status != 200:
                    LOGGER.error(f"Invalid request: {await resp.text()}")
                    return None
                response = await resp.json(content_type=None)
        self.mpd_link = response["MPD"]
        return response["KEY_STRING"]


class Download(SERVICE):

    def __init__(self, name: str, resl: str, mpd: str):
        super().__init__()
        self.mpd_link = mpd
        self.name = self.c_name(name)
        self.vid_format = f'bestvideo.{resl}/bestvideo.2/bestvideo'

        videos_dir = "Videos"
        encrypted_basename = f"{self.name}_enc"
        decrypted_basename = f"{self.name}_dec"

        self.encrypted_video = join(videos_dir, f"{encrypted_basename}.mp4")
        self.encrypted_audio = join(videos_dir, f"{encrypted_basename}.m4a")
        self.decrypted_video = join(videos_dir, f"{decrypted_basename}.mp4")
        self.decrypted_audio = join(videos_dir, f"{decrypted_basename}.m4a")
        self.merged = join(videos_dir, f"{self.name} - {self.get_date()}.mkv")

    async def process_video(self):
        key = await self.get_keys()
        if not key:
            LOGGER.error("Could not retrieve decryption keys.")
            return
        LOGGER.info(f"MPD: {self.mpd_link}")
        LOGGER.info(f"Got the Keys > {key}")
        LOGGER.info(f"Downloading Started...")
        if await self.__yt_dlp_drm() and await self.__decrypt(
                key) and await self.__merge():
            LOGGER.info(f"Cleaning up files for: {self.name}")
            await self.__cleanup_files()
            LOGGER.info(f"Downloading complete for: {self.name}")
            return self.merged
        LOGGER.error(f"Processing failed for: {self.name}")
        return None

    async def __subprocess_call(self, cmd: Union[str, List[str]]):
        if isinstance(cmd, str):
            cmd = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            LOGGER.error(
                f"Command failed: {' '.join(cmd)}\nError: {stderr.decode()}")
            return False
        return True

    async def __yt_dlp_drm(self) -> bool:
        video_download = self.__subprocess_call(
            f'yt-dlp -k --allow-unplayable-formats -f "{self.vid_format}" --fixup never "{self.mpd_link}" --external-downloader aria2c --external-downloader-args "-x 16 -s 16 -k 1M" -o "{self.encrypted_video}"'
        )
        audio_download = self.__subprocess_call(
            f'yt-dlp -k --allow-unplayable-formats -f ba --fixup never "{self.mpd_link}" --external-downloader aria2c --external-downloader-args "-x 16 -s 16 -k 1M" -o "{self.encrypted_audio}"'
        )
        return await asyncio.gather(video_download, audio_download)

    async def __decrypt(self, key: str):
        LOGGER.info("Decrypting...")
        video_decrypt = self.__subprocess_call(
            f'mp4decrypt --show-progress {key} "{self.encrypted_video}" "{self.decrypted_video}"'
        )
        audio_decrypt = self.__subprocess_call(
            f'mp4decrypt --show-progress {key} "{self.encrypted_audio}" "{self.decrypted_audio}"'
        )
        return await asyncio.gather(video_decrypt, audio_decrypt)

    async def __merge(self):
        LOGGER.info("Merging...")
        return await self.__subprocess_call(
            f'ffmpeg -i "{self.decrypted_video}" -i "{self.decrypted_audio}" -c copy "{self.merged}"'
        )

    async def __cleanup_files(self):
        for file_path in [
                self.encrypted_video, self.encrypted_audio,
                self.decrypted_audio, self.decrypted_video
        ]:
            try:
                await remove(file_path)
            except Exception as e:
                LOGGER.warning(f"Failed to delete {file_path}: {str(e)}")


async def main(name, resl, mpd):
    downloader = Download(name, resl, mpd)
    await downloader.process_video()


if __name__ == "__main__":
    print_ascii_art()
    parser = argparse.ArgumentParser(
        description='Download and Decrypt DRM Video via Remote Key API')
    parser.add_argument('-l',
                        '--link',
                        type=str,
                        help='Valid MPD Link',
                        required=True)
    parser.add_argument('-r',
                        '--resl',
                        type=str,
                        help=
                        'Video Resolution (1/2/3) where 1 is highest and 3 is lowest available resolution',
                        default="1")
    parser.add_argument('-o',
                        '--name',
                        type=str,
                        help='Custom name for the output file',
                        default="output")
    args = parser.parse_args()
    asyncio.run(
        main(name=args.name, resl=args.resl, mpd=args.link))
