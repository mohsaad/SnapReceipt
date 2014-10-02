import subprocess
cmd = ["C:/Program Files (x86)/Tesseract-OCR/tesseract.exe", "big.jpg", "rec"]

process = subprocess.Popen(cmd, stderr = subprocess.STDOUT, stdout=subprocess.PIPE)
outputstring = process.communicate()[0]