import logging
from datetime import datetime
from pathlib import Path

# 日志目录
LOG_DIR = Path("./logs")
LOG_DIR.mkdir(exist_ok=True, parents=True)

# 日志文件名（带时间戳）
log_file = LOG_DIR / f"game_dev_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# 导出日志对象
dev_logger = logging.getLogger("game_dev")