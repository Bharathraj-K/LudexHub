from __future__ import annotations

from PySide6.QtCore import QObject, QUrl, Signal, Slot
from PySide6.QtGui import QPixmap, QPixmapCache
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest

from core.paths import get_data_dir

ICONS_DIR = get_data_dir() / "icons"
CDN_BASE = "https://cdn.cloudflare.steamstatic.com/steam/apps"
IMAGE_FILE = "capsule_sm_120.jpg"


class IconLoader(QObject):
    image_ready = Signal(str, QPixmap)

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._nam = QNetworkAccessManager(self)
        self._nam.finished.connect(self._on_reply)
        ICONS_DIR.mkdir(parents=True, exist_ok=True)

    def load_icon(self, appid: str) -> None:
        cache_key = f"steam_{appid}"

        cached = QPixmap()
        if QPixmapCache.find(cache_key, cached):
            self.image_ready.emit(appid, cached)
            return

        disk_path = ICONS_DIR / f"{appid}.jpg"
        if disk_path.exists():
            pixmap = QPixmap(str(disk_path))
            if not pixmap.isNull():
                QPixmapCache.insert(cache_key, pixmap)
                self.image_ready.emit(appid, pixmap)
                return

        url = QUrl(f"{CDN_BASE}/{appid}/{IMAGE_FILE}")
        request = QNetworkRequest(url)
        request.setHeader(QNetworkRequest.UserAgentHeader, "GameLauncher/0.2")
        reply = self._nam.get(request)
        reply.setProperty("appid", appid)

    @Slot(object)
    def _on_reply(self, reply) -> None:
        appid = reply.property("appid")
        reply.deleteLater()

        if reply.error() != reply.NetworkError.NoError:
            return

        data = reply.readAll()
        pixmap = QPixmap()
        if pixmap.loadFromData(data):
            disk_path = ICONS_DIR / f"{appid}.jpg"
            pixmap.save(str(disk_path), "JPEG", 85)

            cache_key = f"steam_{appid}"
            QPixmapCache.insert(cache_key, pixmap)
            self.image_ready.emit(appid, pixmap)
