from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel
import pandas as pd
import json
import os

class JsonToExcelInput(BaseModel):
    """Input schema for JsonToExcelTool."""
    json_file: str  # Path to JSON file
    excel_file: str  # Path to output Excel file

class JsonToExcelTool(BaseTool):
    name: str = "JSON to Excel Converter"
    description: str = (
        "Converts a JSON file containing contract details into an Excel file. "
        "Provide the path to the JSON file and where to save the Excel output."
    )
    args_schema: Type[BaseModel] = JsonToExcelInput

    def _run(self, json_file: str, excel_file: str) -> str:
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(excel_file), exist_ok=True)

            # Read JSON file
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            # Flatten the nested JSON structure
            rows = []
            for section, fields in data.items():
                for field, value in fields.items():
                    rows.append({
                        'Contract Section': section,
                        'Field Name': field,
                        'Value': str(value)  # Convert all values to strings
                    })
            
            # Create DataFrame
            df = pd.DataFrame(rows)
            
            try:
                # First attempt with openpyxl
                with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Contract Details')
            except Exception as e1:
                try:
                    # Second attempt with xlsxwriter
                    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
                        df.to_excel(writer, index=False, sheet_name='Contract Details')
                except Exception as e2:
                    # Last attempt - direct write
                    df.to_excel(excel_file, index=False, sheet_name='Contract Details', engine='openpyxl')
            
            return f"Successfully converted {json_file} to Excel format at {excel_file}"
        except Exception as e:
            return f"Error converting JSON to Excel: {str(e)}" 