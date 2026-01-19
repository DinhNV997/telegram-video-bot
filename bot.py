import os
import re
import tempfile
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, MessageHandler, ContextTypes, filters
import yt_dlp

BOT_TOKEN = os.getenv("BOT_TOKEN")
URL_RE = re.compile(r"(https?://\S+)")

YTDLP_OPTS = {
    "outtmpl": "%(title).60s_%(id)s.%(ext)s",
    "format": "mp4/bestvideo+bestaudio/best",
    "merge_output_format": "mp4",
    "noplaylist": True,
    "quiet": True,
}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    m = URL_RE.search(text)
    if not m:
        return

    url = m.group(1).strip()
    await update.message.reply_text(f"✅ Đã nhận link, đang tải: {url}")
    await context.bot.send_chat_action(update.effective_chat.id, ChatAction.UPLOAD_VIDEO)

    with tempfile.TemporaryDirectory() as tmpdir:
        opts = dict(YTDLP_OPTS)
        opts["paths"] = {"home": tmpdir}

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                if not os.path.exists(filename) and info.get("requested_downloads"):
                    filename = info["requested_downloads"][0]["filepath"]

            with open(filename, "rb") as f:
                await update.message.reply_video(video=f, caption=info.get("title", "Video"))

        except Exception as e:
            await update.message.reply_text(f"❌ Không tải được video. Lỗi: {e}")

def main():
    if not BOT_TOKEN:
        raise RuntimeError("Thiếu BOT_TOKEN. Hãy set BOT_TOKEN trước khi chạy.")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
