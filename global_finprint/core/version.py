from config import settings
import os
from enum import IntEnum


class VersionInfo:
    class Fields(IntEnum):
        jenkins_build = 0
        git_version = 1
        git_hash = 2
        date = 3
        commit_message = 4

    @staticmethod
    def get_version_info():
        version_file = os.path.join(str(settings.common.ROOT_DIR), 'global_finprint', 'static', 'version.txt')
        return list(v for v in open(version_file).read().split('\n') if v)
