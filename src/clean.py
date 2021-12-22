import json
import shutil
from os import read
from pathlib import Path

from loguru import logger

from src.data import DATA_DIR
from src.utils.io import read_json

class OrganizaFiles:
    """
    This class is used to organize files in a directory by
    moving files into directories based on extention.
    """
    def __init__(self, directoy):
        self.directory = Path(directoy)
        if not self.directory.exists():
            raise FileNotFoundError(f"{self.directory} does not exist" )

        ext_dirs = read_json(DATA_DIR / "extensions.json")
        self.extentions_dest = {}
        for dir_naame, ext_list in ext_dirs.items():
            for ext in ext_list:
                self.extentions_dest[ext] = dir_naame
        logger.info(self.extentions_dest)

    def __call__(self):
        """Organize files in a directory by movig them
        to sub directories based on extention.
        """
        logger.info(f"Organiing files in {self.directory}...")
        file_extensions = []
        for file_path in self.directory.iterdir():

            # ignore directories
            if file_path.is_dir():
                continue

            # ignore hidden files
            if file_path.name.startswith('.'):
                continue

            # get all file types
            file_extensions.append(file_path.suffix)

            # move files
            if file_path.suffix not in self.extentions_dest:
                DEST_DIR = self.directory / 'other'

            else:
                DEST_DIR = self.directory / self.extentions_dest[file_path.suffix]

            DEST_DIR.mkdir(exist_ok=True)
            logger.info(f"Moving {file_path} to {DEST_DIR}...")
            shutil.move(str(file_path), str(DEST_DIR))

if __name__ == "__main__":
    org_files = OrganizaFiles('/mnt/c/Users/Dr-laptop/Downloads')
    org_files()
    logger.info("Done!")
