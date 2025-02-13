import os
import shutil
import logging

logger = logging.getLogger("OpenFOAMCaseRunner")

CASES_RUN_DIR = "cases/cases_run/"
TEMPLATE_DIR = "cases/template/"

def create_case_folders(case_id):
    """ Create case folder and copy the necessary templates. """
    case_folder = os.path.join(CASES_RUN_DIR, f"case_{case_id:04d}")

    if os.path.exists(case_folder):
        logger.warning(f"Case {case_id:04d} already exists, skipping copy.")
    else:
        os.makedirs(case_folder, exist_ok=True)
        logger.info(f"Created case folder: {case_folder}")
    
    return case_folder

def copy_template(case_folder, template_source, target_subdir):
    """ Copy the correct template from the source to the case folder. """
    src_path = os.path.join(TEMPLATE_DIR, template_source)
    dest_path = os.path.join(case_folder, target_subdir)

    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)  # Remove previous contents

    shutil.copytree(src_path, dest_path)
    logger.info(f"Copied {template_source} -> {dest_path}")
