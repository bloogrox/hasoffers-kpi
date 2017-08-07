import os


if os.environ.get('ENV_TYPE') == 'ci':
    from .ci import *  # noqa
else:
    try:
        from .local import *  # noqa
    except ImportError:
        from .prod import *  # noqa
