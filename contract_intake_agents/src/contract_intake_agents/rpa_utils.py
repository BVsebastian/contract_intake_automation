import logging
from pathlib import Path
from contract_intake_agents.config.rpa_config import (
    SKIP_RPA_BOTS,
    DOWNLOAD_BOT_PATH,
    UPLOAD_BOT_PATH,
    UIPATH_CLI_PATH
)
from contract_intake_agents.utils.uipath_runner import UiPathRunner

logger = logging.getLogger(__name__)
uipath = UiPathRunner(UIPATH_CLI_PATH)

def download_contracts() -> bool:
    """Execute the Contract Download Bot"""
    if SKIP_RPA_BOTS:
        logger.info("Skipping contract download bot (SKIP_RPA_BOTS=True)")
        return True
        
    logger.info("Executing Contract Download Bot...")
    return uipath.execute_process(DOWNLOAD_BOT_PATH)

def upload_outputs() -> bool:
    """Execute the Contract Output Upload Bot"""
    if SKIP_RPA_BOTS:
        logger.info("Skipping output upload bot (SKIP_RPA_BOTS=True)")
        return True
        
    logger.info("Executing Contract Output Upload Bot...")
    return uipath.execute_process(UPLOAD_BOT_PATH) 