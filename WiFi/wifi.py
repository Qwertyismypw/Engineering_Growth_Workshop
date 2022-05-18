import subprocess as sp
import time
from datetime import datetime

stored_wifi = {}
mins = 5 #how frequent in mins do you want to log
hours = 12 #how many hours do you want to log for
logging_time = 60 * mins
log_count = 60/mins * hours
current_log = 1
#wifi_name = '' #What wifi are we loking for, case sensitive
last_ch = None
path = r'' #where to store file and name it


while current_log <= log_count:
    metrics = sp.run(['netsh',  'wlan',  'show',  'interfaces'], stdout=sp.PIPE).stdout.splitlines()
    current_metrics = []
    for i in metrics:
        i = str(i)
        if 'signal' in i.lower() or 'channel' in i.lower() or 'profile' in i.lower():
            metric, val = i.split("b'")[1].split(':')
            metric = metric.strip()
            val = val.strip("'").strip()
            current_metrics.append(val)
    c, s, n = current_metrics[:]
    s = float(s.strip('%'))
    #print (c,s,n)
    n = '{0} - {1}'.format(n, c)
    if n not in stored_wifi:
        stored_wifi[n] = [1, [[s], datetime.now().strftime("%H:%M:%S")]]
    else:
        stored_wifi[n][0] += 1
        stored_wifi[n][1][0].append(s)
    print (stored_wifi)
    time.sleep(logging_time)
    current_log += 1

with open(path, 'w') as f:
    for key, value in stored_wifi.items():
        f.write('%s:%s\n' % (key, value))
