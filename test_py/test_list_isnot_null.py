a = [1]
b = [{'m': 10}]
c = 0
if a:
    print "a is ok"
else:
    print "a is no"

if b:
    print "b is ok"
else:
    print "b is no"

for i in range(20):
    if i == 10:
        print "Without this xiaoqu in the db."
	continue
    print i
