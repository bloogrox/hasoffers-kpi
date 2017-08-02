import os


if os.environ.get('ENV_TYPE') == 'ci':
    from .ci import *
else:
    try:
        from .local import *
    except ImportError:
        from .prod import *
