import psutil
p=psutil.Process()
print(p.cpu_percent())