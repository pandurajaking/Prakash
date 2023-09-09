import subprocess
import datetime
import json
import asyncio
import os
import requests
import time
from p_bar import progress_bar
import aiohttp
import tgcrypto
import aiofiles
import helper
from pyrogram.types import Message
from pyrogram import Client, filters
from subprocess import getstatusoutput
from tqdm import tqdm
MAX_RETRIES = 5

def retry(func):
    async def wrapper(*args, **kwargs):
        for attempt in range(MAX_RETRIES):
            try:
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
                return result
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    print(f"Attempt {attempt + 1} failed with error: {e}")
                    print("Retrying...")
                else:
                    raise
    return wrapper






def duration(filename):
    for attempt in range(MAX_RETRIES):
        try:
            result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                     "format=duration", "-of",
                                     "default=noprint_wrappers=1:nokey=1", filename],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT,
                                    check=True, text=True)
            return float(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Attempt {attempt + 1} failed with error: {e.stdout}")
            if attempt < MAX_RETRIES - 1:
                print("Retrying...")
                time.sleep(1)  # Add a delay before retrying
            else:
                raise
        except ValueError:
            print(f"Attempt {attempt + 1} failed: Unable to parse duration as a float")
            if attempt < MAX_RETRIES - 1:
                print("Retrying...")
                time.sleep(1)  # Add a delay before retrying
            else:
                raise
@retry
async def aio(url, name):
    k = f'{name}.pdf'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(k, mode='wb')
                await f.write(await resp.read())
                await f.close()
    return k


@retry
async def download(url, name):
    ka = f'{name}.pdf'
    max_retries = 5  # Set the maximum number of retries to 5
    for retry_count in range(max_retries):  # Retry up to 5 times
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    try:
                        f = await aiofiles.open(ka, mode='wb')
                        await f.write(await resp.read())
                        await f.close()
                        return ka  # Return the downloaded file path
                    except Exception as e:
                        print(f"Error during 'write' operation: {e}")
                        # Handle the error condition, you can log or raise an exception here
                else:
                    print(f"Download failed with status code: {resp.status}")
                    # Handle the download failure, you can log or raise an exception here

        # Sleep for a moment before retrying
        await asyncio.sleep(5)

    # If all retries fail, return None (or another appropriate value)
    return None





def parse_vid_info(info):
    info = info.strip()
    info = info.split("\n")
    new_info = []
    temp = []
    for i in info:
        i = str(i)
        if "[" not in i and '---' not in i:
            while "  " in i:
                i = i.replace("  ", " ")
            i.strip()
            i = i.split("|")[0].split(" ",2)
            try:
                if "RESOLUTION" not in i[2] and i[2] not in temp and "audio" not in i[2]:
                    temp.append(i[2])
                    new_info.append((i[0], i[2]))
            except:
                pass
    return new_info


def vid_info(info):
    info = info.strip()
    info = info.split("\n")
    new_info = dict()
    temp = []
    for i in info:
        i = str(i)
        if "[" not in i and '---' not in i:
            while "  " in i:
                i = i.replace("  ", " ")
            i.strip()
            i = i.split("|")[0].split(" ",3)
            try:
                if "RESOLUTION" not in i[2] and i[2] not in temp and "audio" not in i[2]:
                    temp.append(i[2])
                    
                    # temp.update(f'{i[2]}')
                    # new_info.append((i[2], i[0]))
                    #  mp4,mkv etc ==== f"({i[1]})" 
                    
                    new_info.update({f'{i[2]}':f'{i[0]}'})

            except:
                pass
    return new_info



@retry
async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if proc.returncode == 1:
        return False
    if stdout:
        return f'[stdout]\n{stdout.decode()}'
    if stderr:
        return f'[stderr]\n{stderr.decode()}'

    
    
    
def old_download(url, file_name):
    if os.path.exists(file_name):
        os.remove(file_name)

    r = requests.get(url, allow_redirects=True, stream=True)
    total_size = int(r.headers.get('content-length', 0))

    with open(file_name, 'wb') as fd, tqdm(
        desc=file_name,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in r.iter_content(chunk_size=1024):
            bar.update(len(data))
            fd.write(data)

    print("Download completed.")

def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size < 1024.0 or unit == 'PB':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"


def time_name():
    date = datetime.date.today()
    now = datetime.datetime.now()
    current_time = now.strftime("%H%M%S")
    return f"{date} {current_time}.mp4"

@retry
async def download_video(url, cmd, name):
    download_cmd = f"{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args 'aria2c: -x 16 -j 32'"
    for attempt in range(MAX_RETRIES):
        try:
            # Execute the download command asynchronously
            proc = await asyncio.create_subprocess_shell(
                download_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            # Wait for the download to complete
            _, stderr = await proc.communicate()

            if proc.returncode == 0:
                # Check if the downloaded file exists
                if os.path.isfile(name):
                    return name
                elif os.path.isfile(f"{name}.webm"):
                    return f"{name}.webm"
                name = name.split(".")[0]
                if os.path.isfile(f"{name}.mkv"):
                    return f"{name}.mkv"
                elif os.path.isfile(f"{name}.mp4"):
                    return f"{name}.mp4"
                elif os.path.isfile(f"{name}.mp4.webm"):
                    return f"{name}.mp4.webm"
                return name
            else:
                error_msg = stderr.decode() if stderr else "No error message available"
                logging.error(f"Download failed with error: {error_msg}")
                if attempt < MAX_RETRIES - 1:
                    print(f"Attempt {attempt + 1} failed. Retrying...")
                else:
                    raise Exception("Download failed after multiple attempts")
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                print(f"Attempt {attempt + 1} failed with error: {e}")
                print("Retrying...")
            else:
                raise


@retry
async def send_doc(bot: Client, m: Message, cc, ka, cc1, prog, count, name):
    reply = await m.reply_text(f"Uploading - `{name}`")
    time.sleep(1)
    start_time = time.time()
    await m.reply_document(ka, caption=cc1)
    count += 1
    await reply.delete(True)
    time.sleep(1)
    os.remove(ka)
    time.sleep(3)

@retry
async def send_vid(bot: Client, m: Message, cc, filename, thumb, name, prog):
    subprocess.run(f'ffmpeg -i "{filename}" -ss 00:00:12 -vframes 1 "{filename}.jpg"', shell=True)
    await prog.delete(True)
    reply = await m.reply_text(f"**Uploading ...** - `{name}`")
    try:
        if thumb == "no":
            thumbnail = f"{filename}.jpg"
        else:
            thumbnail = thumb
    except Exception as e:
        await m.reply_text(str(e))

    dur = int(duration(filename))

    start_time = time.time()

    try:
        await m.reply_video(filename, caption=cc, supports_streaming=True, height=720, width=1280, thumb=thumbnail, duration=dur, progress=progress_bar, progress_args=(reply, start_time))
    except Exception:
        await m.reply_document(filename, caption=cc, progress=progress_bar, progress_args=(reply, start_time))

    os.remove(filename)
    os.remove(f"{filename}.jpg")
    await reply.delete(True)

    
def get_video_attributes(file: str):
    """Returns video duration, width, height"""

    class FFprobeAttributesError(Exception):
        """Exception if ffmpeg fails to generate attributes"""

    cmd = (
        "ffprobe -v error -show_entries format=duration "
        + "-of default=noprint_wrappers=1:nokey=1 "
        + "-select_streams v:0 -show_entries stream=width,height "
        + f" -of default=nw=1:nk=1 '{file}'"
    )
    res, out = getstatusoutput(cmd)
    if res != 0:
        raise FFprobeAttributesError(out)
    width, height, dur = out.split("\n")
    return (int(float(dur)), int(width), int(height))
