import os
import subprocess
import logging

logger = logging.getLogger(__name__)

class UiPathRunner:
    """Utility class to run UiPath processes"""
    
    def __init__(self, uipath_path: str = "C:\\Users\\bened\\AppData\\Local\\Programs\\UiPath\\Studio\\UiRobot.exe"):
        self.uipath_path = uipath_path
        
    def execute_process(self, process_file: str) -> bool:
        """
        Execute a UiPath process
        Args:
            process_file: Path to the .nupkg file to execute
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not os.path.exists(self.uipath_path):
                logger.error(f"UiRobot.exe not found at {self.uipath_path}")
                return False

            if not os.path.exists(process_file):
                logger.error(f"Process file not found at: {process_file}")
                return False

            cmd_str = f'"{self.uipath_path}" execute --file "{process_file}"'
            logger.info(f"Executing UiPath process: {process_file}")
            
            result = subprocess.run(cmd_str, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("UiPath process executed successfully")
                return True
            else:
                logger.error(f"UiPath process failed: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"Error executing UiPath process: {str(e)}")
            return False 