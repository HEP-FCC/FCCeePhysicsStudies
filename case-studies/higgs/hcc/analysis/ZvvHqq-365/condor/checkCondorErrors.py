import subprocess
#result = subprocess.run(["ls -l std/*.err | awk '$5>1000'"], stdout=subprocess.PIPE).stdout.decode()
result = subprocess.check_output("ls -l std/*.err | awk '$5>1010'", shell=True).decode().split("\n")
for line in result:
    if (line != ""):
        err = line.split()[-1]
        print("Possible error in file", err)
        log = err[:-4]+".out"
        rootfile = subprocess.run(["grep", "events_", log], stdout=subprocess.PIPE).stdout.decode().split()[2][:-1]
        sample = rootfile.split("/")[-2]
        print("-> sample:", sample)
        print("-> input file:", rootfile)
        print()
