import subprocess as subp
fang_url = "http://123"
shell_mail_cmd = 'echo "' + fang_url + '" | mail -s "new good fang url" zmqtb2008@126.com'
subp.Popen(shell_mail_cmd, stdout=subp.PIPE, stderr=subp.PIPE, shell=True)
