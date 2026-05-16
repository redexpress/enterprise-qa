import os
import logging
import logging.config
from pathlib import Path

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


ROOT = Path(__file__).resolve().parents[4]

# 默认配置
DEFAULT_CONFIG = {
    'database': {
        'type': 'sqlite',
        'path': str(ROOT / 'enterprise.db')
    },
    'knowledge_base': {
        'root_path': str(ROOT / 'knowledge'),
        'index_type': 'bm25'
    },
    'timezone': 'Asia/Shanghai',
    'logging': {
        'level': 'WARNING',
        'file': './logs/enterprise-qa.log'
    }
}


# Load config file
def load_config() -> dict:
    config = DEFAULT_CONFIG.copy()

    # 尝试从 config.yaml 读取
    config_path = ROOT / 'config.yaml'
    if config_path.exists() and HAS_YAML:
        with open(config_path, 'r', encoding='utf-8') as f:
            user_config = yaml.safe_load(f)
            if user_config:
                config.update(user_config)

    return config


CONFIG = load_config()

# 数据库配置
DB_TYPE = CONFIG['database']['type']
DB_PATH = os.environ.get("ENTERPRISE_QA_DB_PATH") or CONFIG['database']['path']

# 知识库配置
KB_PATH = os.environ.get("ENTERPRISE_QA_KB_PATH") or CONFIG['knowledge_base']['root_path']
KB_INDEX_TYPE = CONFIG.get('knowledge_base', {}).get('index_type', 'bm25')

# 时区配置
TIMEZONE = CONFIG.get('timezone', 'Asia/Shanghai')

# 日志配置
LOG_LEVEL = os.environ.get("ENTERPRISE_QA_LOG_LEVEL") or CONFIG['logging']['level']
LOG_FILE = os.environ.get("ENTERPRISE_QA_LOG_FILE") or CONFIG['logging']['file']


def setup_logging() -> logging.Logger:
    """初始化日志配置"""
    log_dir = Path(LOG_FILE).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'level': LOG_LEVEL
            },
            'file': {
                'class': 'logging.FileHandler',
                'filename': LOG_FILE,
                'formatter': 'standard',
                'level': LOG_LEVEL,
                'encoding': 'utf-8'
            }
        },
        'root': {
            'level': LOG_LEVEL,
            'handlers': ['console', 'file']
        }
    })

    return logging.getLogger(__name__)
