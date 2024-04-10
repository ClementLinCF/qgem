import os
import sys
import re
import subprocess

class MatrixMultiplier:
    def __init__(self, PRECISION_A, PRECISION_B, PRECISION_C, COMPUTE_PRECISION,
                 OP_A, OP_B, M, N, K, LDA, LDB, LDC, BATCH_COUNT, TIME_SPAN, EX):
        self.PRECISION_A = PRECISION_A
        self.PRECISION_B = PRECISION_B
        self.PRECISION_C = PRECISION_C
        self.COMPUTE_PRECISION = COMPUTE_PRECISION
        self.OP_A = OP_A
        self.OP_B = OP_B
        self.M = int(M)
        self.N = int(N)
        self.K = int(K)
        self.LDA = int(LDA)
        self.LDB = int(LDB)
        self.LDC = int(LDC)
        self.BATCH_COUNT = int(BATCH_COUNT)
        self.TIME_SPAN = int(TIME_SPAN)
        self.TIME_SPAN = int(TIME_SPAN)
        self.EX = EX
    def execute_program(self):
        # Set environment variables
        os.environ['ROCBLAS_LAYER'] = '6'
        os.environ['TENSILE_DB'] = '0x8016'

        # Prepare program arguments
        program_args = [
            './gemm',
            self.PRECISION_A, self.PRECISION_B, self.PRECISION_C, self.COMPUTE_PRECISION,
            self.OP_A, self.OP_B,
            str(self.M), str(self.N), str(self.K),
            str(self.LDA), str(self.LDB), str(self.LDC),
            str(self.BATCH_COUNT), str(self.TIME_SPAN), self.EX
        ]

        # Execute the program with subprocess
        subprocess.run(program_args)

    def check_mnk(self):

        # Define the regular expression pattern to match the desired values
        pattern = r'-m\s+(\d+).*-n\s+(\d+).*-k\s+(\d+).*--lda\s+(\d+).*--ldb\s+(\d+).*--ldc\s+(\d+)'

        # Read from the log file
        with open('qgemm_tmp.log', 'r') as log_file:
            log_string = log_file.read()

        # Find all matches in the log string
        matches = re.findall(pattern, log_string)
            
        # os.remove('qgemm_tmp.log')

        with open('qgemm.log', 'w') as output_file:
            if matches:
                for match in matches:
                    m_value = int(match[0])
                    n_value = int(match[1])
                    k_value = int(match[2])
                    lda_value = int(match[3])
                    ldb_value = int(match[4])
                    ldc_value = int(match[5])

                    if (m_value == self.M and
                        n_value == self.N and
                        k_value == self.K and
                        lda_value == self.LDA and
                        ldb_value == self.LDB and
                        ldc_value == self.LDC):
                        output_file.write("ok\n")
                    else:
                        output_file.write(f"m_value: {m_value} vs self.M: {self.M}")
                        output_file.write(f"n_value: {n_value} vs self.N: {self.N}")
                        output_file.write(f"k_value: {k_value} vs self.K: {self.K}")
                        output_file.write(f"lda_value: {lda_value} vs self.LDA: {self.LDA}")
                        output_file.write(f"ldb_value: {ldb_value} vs self.LDB: {self.LDB}")
                        output_file.write(f"ldc_value: {ldc_value} vs self.LDC: {self.LDC}")

            else:
                output_file.write("Pattern not found in the log file.")

    def get_TFLOPS(self):
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
            # print(f"The maximum number divided by 1000 is: {max_number}")

            # Delete the log file after processing
            # os.remove('qgemm_tmp.log')
            return max_number
        else:
            # print("No matching numbers found in the log file.")
            return .0



def main(args):
    if len(args) < 14:
        print("Usage: python qgemm.py PRECISION_A PRECISION_B PRECISION_C COMPUTE_PRECISION OP_A OP_B M N K LDA LDB LDC BATCH_COUNT TIME_SPAN")
        return

    precision_a, precision_b, precision_c, compute_precision, op_a, op_b, m, n, k, lda, ldb, ldc, batch_count, time_span, ex = args

    instance = MatrixMultiplier(precision_a, precision_b, precision_c, compute_precision,
                                op_a, op_b, m, n, k, lda, ldb, ldc, batch_count, time_span, ex)

    instance.execute_program()
    instance.check_mnk()

if __name__ == "__main__":
    main(sys.argv[1:])





# Example usage
# instance = MatrixMultiplier('R_32F', 'R_32F', 'R_32F', 'R_32F', 'OP_N', 'OP_T', 8640, 8640, 8640, 8640, 8640, 8640, 72, 300)
# instance.execute_program()
# instance.check_mnk()

# tflops = instance.get_TFLOPS()

# with open('qgemm.log', 'w') as output_file:
#     output_file.write("QQQQQQ")
#     output_file.write(tflops)



# os.remove('qgemm_tmp.log')