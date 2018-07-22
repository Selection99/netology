from subprocess import Popen

string = 'open -a Safari'
p = Popen(string.split())
print(p.args)