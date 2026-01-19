import os
import re
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

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

# ---- mini web server để Render thấy có PORT ----
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"OK")

def run_http_server():
    port = int(os.getenv("PORT", "10000"))
    server = HTTPServer(("0.0.0.0", port), HealthHan
