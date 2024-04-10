import subprocess

# Define the command with parameters
command = ['python3', 'qgemm.py', 'R_32F', 'R_32F', 'R_32_F', 'R_32F', 'OP_N', 'OP_T',
           '8640', '8640', '8640', '8640', '8640', '8640', '72', '300']

# Run qgemm.py with parameters and redirect stdout and stderr to qgemm_tmp.log
with open('qgemm_tmp.log', 'w') as logfile:
    subprocess.run(command, stdout=logfile, stderr=subprocess.STDOUT, check=True)

