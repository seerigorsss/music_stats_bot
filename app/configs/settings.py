import logging
import os
import sys

from configs.env_configs_models import EnvConfigsModel
from dotenv import load_dotenv
from pydantic.error_wrappers import ValidationError

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
root_logger = logging.getLogger()
_logger = logging.getLogger(__name__)

root_logger.setLevel(logging.INFO)
load_dotenv(dotenv_path=os.path.join('configs', '.env'))

try:
    env_parameters = EnvConfigsModel(**os.environ)
except ValidationError as e:
    _logger.critical(exc_info=e, msg='Env parameters validation')
    sys.exit(-1)
