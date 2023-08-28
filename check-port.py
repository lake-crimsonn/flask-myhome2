import psutil
sockets = psutil.net_connections()
for s in sockets:
    if 'port=5001' in str(s):
        print(s)
