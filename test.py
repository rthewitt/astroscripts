#!/usr/bin/python
#print 'Content-type: text/html\n'
print 'Starting loop\n'
import subprocess
import os
import io
from select import poll, POLLIN

#r_fd, w_fd = os.pipe()

# Externally created for now
# has always been io, but later we reached a collision so I'm specifying
#pipein = io.open('../data/courseQ','r')
pipe_d = os.open('../data/courseQ', os.O_RDONLY)

p = poll()
#p.register(r_fd, POLLIN)
p.register(pipe_d, POLLIN)

#No necessary, will write externally
#os.write(w_fd, 'X') # Put something in the pipe so p.poll() will return

while True:
    events = p.poll(100)
    for e in events:
        print e
        os.read(pipe_d, 1)

#print """<html><head>
#<title>%s</title>
#</head><body>"""
#subprocess.call(['./setup-class.sh','CS997'])
#print """</body>
#</html>"""
