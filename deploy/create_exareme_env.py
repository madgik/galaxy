from __future__ import print_function
import os

exIP = os.environ['EXAREME_IP'];
exPort = os.environ['EXAREME_PORT'];

filename = "/srv/executor/tools/exaremeTools/exareme_environment.py";
dirname = os.path.dirname(filename);

if not os.path.exists(dirname):
    os.makedirs(dirname)


out_file = open(filename,"w");

print('EXAREME_IP =', exIP , file = out_file);
print('EXAREME_PORT = ', exPort, file = out_file);
