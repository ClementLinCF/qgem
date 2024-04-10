import subprocess
import re
import os


def execute_program(command):
    try:
        # Run qgemm.py with parameters and redirect stdout and stderr to qgemm_tmp.log
        with open('qgemm_tmp.log', 'w') as logfile:
            subprocess.run(command, stdout=logfile, stderr=subprocess.STDOUT, check=True)


    except subprocess.CalledProcessError as e:
        print(f"Error running qgemm.py: {e}")

def get_TFLOPS():
    # Read from the log file
    with open('qgemm_tmp.log', 'r') as log_file:
        log_lines = log_file.readlines()

    # Define a regular expression pattern to match floating-point numbers
    pattern = r'\s+(\d+\.\d+)'

    # List to store the first numbers from each line that matches the pattern
    numbers = []

    # Iterate through each line in the log file
    for line in log_lines:
        match = re.search(pattern, line)
        if match:
            number = float(match.group(1))
            numbers.append(number)

    # Check if any numbers were found
    if numbers:
        # Find the maximum number from the list and divide it by 1000
        max_number = max(numbers) / 1000
        print(f"The maximum number divided by 1000 is: {max_number}")
        return max_number
        # Delete the log file after processing
        os.remove('qgemm_tmp.log')
    else:
        print("No matching numbers found in the log file.")

def produce_report(command, tflops, peak_tflops):
    column_names = ['PRECISION_A', 'PRECISION_B', 'PRECISION_C', 'COMPUTE_PRECISION',
                    'OP_A', 'OP_B', 'M', 'N', 'K', 'LDA', 'LDB', 'LDC', 'BATCH_COUNT',
                    'TIME_SPAN', 'TFLOPS', 'PEAK_TFLOPS']
    # Create a new Excel workbook and select the active sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = command[2]  # Set the page name as the third element of the command

    # Write column names to the first row of the sheet
    for col, column_name in enumerate(column_names, start=1):
        sheet.cell(row=1, column=col, value=column_name)

    # Write command data to the second row of the sheet
    for col, value in enumerate(command, start=1):
        sheet.cell(row=2, column=col, value=value)

    # Write TFLOPS and PEAK_TFLOPS values to the second row of the sheet
    sheet.cell(row=2, column=len(command) + 1, value=tflops)
    sheet.cell(row=2, column=len(command) + 2, value=peak_tflops)

    # Save the Excel workbook
    workbook.save('output.xlsx')



peak_tflops = 24.6
# Define the command with parameters
command = ['python3', 'qgemm.py', 'R_32F', 'R_32F', 'R_32F', 'R_32F', 'OP_N', 'OP_T',
           '8640', '8640', '8640', '8640', '8640', '8640', '72', '300']

execute_program(command)
tflops = get_TFLOPS()

produce_report(command, tflops, peak_tflops)
