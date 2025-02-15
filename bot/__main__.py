from pyrogram import filters
from bot import app, data, sudo_users, log_channel
from bot.helper.utils import add_task

video_mimetype = [
  "video/x-flv",
  "video/mp4",
  "video/mkv",
  "application/x-mpegURL",
  "video/MP2T",
  "video/3gpp",
  "video/quicktime",
  "video/x-msvideo",
  "video/x-ms-wmv",
  "video/x-matroska",
  "video/webm",
  "video/x-m4v",
  "video/quicktime",
  "video/mpeg"
  ]

@app.on_message(filters.incoming & filters.command(['start', 'help']))
def help_message(app, message):
    message.reply_text(f"Hi {message.from_user.mention()}\nI can encode Telegram files in x265, just send me a video.", quote=True)
    app.send_message(log_channel, f"**New User Joined:** \n\nUser [{message.from_user.first_name}](tg://user?id={message.from_user.id}) started Bot!!")

@app.on_message(filters.user(sudo_users) & filters.incoming & (filters.video | filters.document))
def encode_video(app, message):
    trace_msg = None
    if log_channel:
      try:
        file = message.forward(chat_id=log_channel)
            #trace_msg = file.reply_text(f"**User Name:** {message.from_user.mention(style="md")}\n\n**User Id:** `{message.from_user.id}`")
      
    if message.document:
      if not message.document.mime_type in video_mimetype:
        message.reply_text("```Invalid Video !\nMake sure its a valid video file.```", quote=True)
        return
    message.reply_text("```Added to queue...```", quote=True)
    data.append(message)
    if len(data) == 1:
      add_task(message)

app.run()
