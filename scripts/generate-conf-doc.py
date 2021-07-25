import yaml
from mlservefast.config import GCONFIG


print(yaml.safe_dump(GCONFIG.settings, indent=2))
