# Huawei Inventory Analysis Tool

## Overview

The **Huawei Inventory Analysis Tool** is designed to compare and analyze inventory reports generated by Huawei for MTN Irancell. By tracking changes based on serial numbers, this tool helps managers detect changes in the network effectively, manage items, and identify any suspicious activities.

## Features

- **Comparison and Analysis**: Compare inventory reports across different dates to detect new, moved, swapped, and removed items.
- **Detailed Reporting**: Generate detailed reports on the status of each item, including additional information extracted from the inventory files.
- **Concurrency**: Leverage multi-threading for efficient data processing.
- **Progress Feedback**: Real-time progress display using a progress bar.
- **Customizable Analysis**: Specific modules for detailed analysis of certain items, such as boards.

## Requirements

To run this project, you will need to have Python installed along with the following libraries:

- `pandas`
- `tqdm`
- `concurrent.futures`
- `openpyxl`
- `xlsxwriter`

You can install these dependencies using the provided `requirements.txt` file.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/codedpro/Huawei-Inventory-Analysis-Tool.git
   cd Huawei-Inventory-Analysis-Tool
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Prepare Inventory Reports**: Ensure the Huawei inventory reports are placed in the specified date folders (e.g., `04_05_2024/Huawei_Inventory_Board.csv`).

2. **Run the Comparison Script**:
   ```bash
   python compare_inventory.py
   ```

3. **Generate Detailed Analysis**: For specific analysis, such as boards, run the additional analysis script:
   ```bash
   python board_analysis.py
   ```

4. **Verification**: Use the finder script to verify specific cases in the inventory reports:
   ```bash
   python finder.py
   ```

## Main Comparison Script

The main comparison script (`compare_inventory.py`) reads the inventory files for different dates, cleans and processes the data, and compares the items based on their serial numbers. It then generates a comprehensive report highlighting the status of each item.

## Detailed Board Analysis

The detailed board analysis script (`board_analysis.py`) provides extra analysis for board items, detecting replaced items and ensuring data consistency. This script produces an Excel report with the original data and replaced items, removing any matching rows to avoid duplication.

## Finder Script

The finder script (`finder.py`) helps verify specific cases by searching for particular serial numbers or other keywords within the CSV files. This ensures the tool's accuracy and effectiveness in detecting changes.

## Example

To compare inventory reports for three dates and generate a report, ensure your CSV files are named appropriately and placed in their respective date folders. Then, run the comparison script:

```bash
python compare_inventory.py
```

To perform additional analysis on board items, run:

```bash
python board_analysis.py
```

To search for a specific serial number in a CSV file, use the finder script:

```bash
python finder.py
```

## Contributing

We welcome contributions to enhance the functionality and usability of this tool. Feel free to open issues or submit pull requests on GitHub.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgements

This tool was developed to streamline the process of comparing and analyzing Huawei inventory reports for MTN Irancell, enabling efficient management and monitoring of fiber optic services and network changes.