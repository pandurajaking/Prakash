

@Client.on_message(filters.command(["pro_jw"]))
async def account_login(bot: Client, m: Message):
    user = m.from_user.id if m.from_user is not None else None
    if user is not None and user not in sudo_users:
        await m.reply("**TUM BHOSADI WALE NIKKAL LO**", quote=True)
        return

    await m.reply_text(
        "Hello @Prakash_Baraiya **I am jw Downloader Bot**. I can download videos from **text** file one by one.**\n\nLanguage** : Python**\nFramework** :Pyrogram\n\nSend **TXT** File {Name : Link}"
    )

    input: Message = await bot.listen(m.chat.id)
    x = await input.download()
    await input.delete(True)

    path = f"./downloads/{m.chat.id}"

    try:
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split(":", 1))
        os.remove(x)
    except Exception as e:
        await m.reply_text("Invalid file input.")
        os.remove(x)
        return

    await m.reply_text(f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **0**")

    input1: Message = await bot.listen(m.chat.id)
    raw_text = input1.text

    try:
        arg = int(raw_text)
    except Exception as e:
        await m.reply_text("Invalid input for starting index. Assuming start index is 0.")
        arg = 0

    editable = await m.reply_text("**Enter Title**")
    input0: Message = await bot.listen(m.chat.id)
    raw_text0 = input0.text

    await m.reply_text("**Enter resolution**")

    input2: Message = await bot.listen(m.chat.id)
    raw_text2 = input2.text

    try:
        resolution = int(raw_text2)
        if resolution < 144 or resolution > 2160:
            raise ValueError
    except ValueError:
        await m.reply_text("Invalid input for resolution. Please enter a valid number between 144 and 2160.")
        return

    editable4 = await m.reply_text("Now send the **Thumb url**\nEg : ```https://telegra.ph/file/d9e24878bd4aba05049a1.jpg```\n\nor Send **no**")
    input6 = await bot.listen(m.chat.id)
    thumb_url = input6.text

    thumb = download_thumbnail(thumb_url)

    count = arg + 1
    try:
        for i in range(arg, len(links)):
            url = links[i][1]
            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").strip()

            if "videos.classplus" in url:
                headers = {
                    'Host': 'api.classplusapp.com',
                    'x-access-token':
                    'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MzgzNjkyMTIsIm9yZ0lkIjoyNjA1LCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTcwODI3NzQyODkiLCJuYW1lIjoiQWNlIiwiZW1haWwiOm51bGwsImlzRmlyc3RMb2dpbiI6dHJ1ZSwiZGVmYXVsdExhbmd1YWdlIjpudWxsLCJjb3VudHJ5Q29kZSI6IklOIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJpYXQiOjE2NDMyODE4NzcsImV4cCI6MTY0Mzg4NjY3N30.hM33P2ai6ivdzxPPfm01LAd4JWv-vnrSxGXqvCirCSpUfhhofpeqyeHPxtstXwe0',
                    'user-agent': 'Mobile-Android',
                    'app-version': '1.4.37.1',
                    'api-version': '18',
                    'device-id': '5d0d17ac8b3c9f51',
                    'device-details':
                    '2848b866799971ca_2848b8667a33216c_SDK-30',
                    'accept-encoding': 'gzip',
          }

                params = {'url': url}
                response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
                url1 = response.json().get('url', url)
            else:
                url1 = url

            name = f'{str(count).zfill(3)}) {name1}'
            Show = f"**Downloading:-**\n\n**Name :-** `{name}`\n\n**Url :-** `{url1}`"
            prog = await m.reply_text(Show)

            try:
                ydl_opts = {
                    'outtmpl': f"{name}.%(ext)s",
                    'format': f"bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]",
                    'quiet': True,
                    'merge_output_format': 'mkv',
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url1, download=False)
                    if 'entries' in info_dict:
                        info_dict = info_dict['entries'][0]

                    filename = ydl.prepare_filename(info_dict)

                    ydl.download([url1])

                thumbnail_file = f"{filename}.jpg"
                subprocess.run(
                    f'ffmpeg -i "{filename}" -ss 00:01:00 -vframes 1 "{thumbnail_file}"',
                    shell=True
                )
                await prog.delete(True)

                cc = f'**Title ┬╗** {name1}.mkv\n**Caption ┬╗** {raw_text0}\n**Index ┬╗** {str(count).zfill(3)}\n\n**Download BY** :- @Prakash_Baraiya'
                dur = int(ydl.calc_duration(info_dict))

                start_time = time.time()
                if "pdf" in url1:
                    await m.reply_document(filename, caption=cc)
                else:
                    await m.reply_video(
                        filename,
                        supports_streaming=True,
                        height=720,
                        width=1280,
                        caption=cc,
                        duration=dur,
                        thumb=thumbnail_file if thumb is None else thumb,
                        progress=progress_bar,
                        progress_args=(m.text, start_time)
                    )
                count += 1
                os.remove(filename)
                os.remove(thumbnail_file)
                await prog.delete(True)
                time.sleep(1)
            except Exception as e:
                await m.reply_text(f"**downloading failed ❌**\n{str(e)}\n**Name** - {name}\n**Link** - `{url}` & `{url1}`")
                continue
    except Exception as e:
        await m.reply_text(str(e))

    await m.reply_text("Done")
