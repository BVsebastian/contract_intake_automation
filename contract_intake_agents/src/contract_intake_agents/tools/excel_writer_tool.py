from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel
import pandas as pd
import json
import os

class ExcelWriterInput(BaseModel):
    """Input schema for ExcelWriterTool."""
    json_file: str  # Path to JSON file
    excel_file: str  # Path to output Excel file

class ExcelWriterTool(BaseTool):
    name: str = "Excel Writer"
    description: str = (
        "Creates a properly formatted Excel file from JSON data. "
        "Provide the path to the JSON file and where to save the Excel output."
    )
    args_schema: Type[BaseModel] = ExcelWriterInput

    def _run(self, json_file: str, excel_file: str) -> str:
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(excel_file), exist_ok=True)

            # Read JSON file
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            # Create rows for DataFrame
            rows = []
            # Handle both list and dict formats
            if isinstance(data, dict):
                for section, fields in data.items():
                    if isinstance(fields, dict):
                        for field, value in fields.items():
                            rows.append({
                                'Contract Section': section,
                                'Field Name': field,
                                'Value': str(value)
                            })
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        rows.append({
                            'Contract Section': item.get('section', ''),
                            'Field Name': item.get('field', ''),
                            'Value': str(item.get('value', ''))
                        })
            
            # Create DataFrame
            df = pd.DataFrame(rows)
            
            # Write to Excel with proper formatting
            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Contract Details')
                
                # Get the worksheet
                worksheet = writer.sheets['Contract Details']
                
                # Auto-adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column = [cell for cell in column]
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(cell.value)
                        except:
                            pass
                    adjusted_width = (max_length + 2)
                    worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
            
            return f"Successfully created Excel file at {excel_file}"
        except Exception as e:
            return f"Error creating Excel file: {str(e)}" 