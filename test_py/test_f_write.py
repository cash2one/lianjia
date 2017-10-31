from time import sleep
for i in range(100):
    f = open('t.txt', 'a')
    f.write(str(i) + '\n')
    sleep(1)
    f.close()
