import os
import yaml

__PROJECT_ROOT_PATH = os.getcwd()
__YAML_CONFIGS = [
    os.path.join(__PROJECT_ROOT_PATH, 'conf', 'django_conf.yaml'),
    os.path.join(__PROJECT_ROOT_PATH, 'conf', 'celery_conf.yaml')
]
YAML_CONFIGS_INFO = {}

for yaml_config in __YAML_CONFIGS:
    with open(yaml_config, 'r', encoding='utf-8') as f:
        __config = yaml.safe_load(f)  # 安全加载方法
        YAML_CONFIGS_INFO.update(__config if __config else {})
