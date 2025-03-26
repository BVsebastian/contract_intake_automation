# RPA Bot Configuration
SKIP_RPA_BOTS = False  # Set to True to skip bot execution during testing
MAX_RETRIES = 3  # Number of times to retry bot execution on failure
RETRY_DELAY = 5  # Seconds to wait between retries

# Bot package paths
DOWNLOAD_BOT_PATH = r"C:\Users\bened\OneDrive\Desktop\Contract_Intake_Automation\contract_download_bot\ContractDownloadBot.1.0.2.nupkg"
UPLOAD_BOT_PATH = r"C:\Users\bened\OneDrive\Desktop\Contract_Intake_Automation\contract_output_upload_bot\ContractOutputUploadBot.1.0.1.nupkg"

# UiPath Configuration
# Try these common installation paths
UIPATH_CLI_PATH = r"C:\Users\bened\AppData\Local\Programs\UiPath\Studio\UiRobot.exe"  # Default path
# Alternative paths if default doesn't exist:
# r"C:\Users\bened\AppData\Local\Programs\UiPath\Studio\UiRobot.exe"
# r"C:\Users\bened\AppData\Local\UiPath\app-{version}\UiRobot.exe" 