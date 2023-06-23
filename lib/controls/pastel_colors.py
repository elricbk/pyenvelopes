import hashlib
from PySide6.QtGui import QColor

class PastelColors:
    full_list = list(
        QColor.fromHsv(h, s, 255) for h in range(0, 360, 30) for s in (20, 60)
    )

    @staticmethod
    def color_for_string(s):
        h = int(hashlib.md5(s.encode('utf-8')).hexdigest(), 16)
        return PastelColors.full_list[h % len(PastelColors.full_list)]

