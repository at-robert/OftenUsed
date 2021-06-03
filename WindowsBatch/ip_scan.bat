FOR /L %i IN (1,1,254) DO ping -n 1 192.168.12.%i  >> z:\Downloads\ipaddresses.txt


PAUSE