import subprocess

expression = "3 + 7 * 2"

process = subprocess.Popen(['python', 'main.py', expression],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)

stdout, stderr = process.communicate()

print(stdout.decode())
print(stderr.decode())