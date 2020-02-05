daemon = False
# 어디서 시작할 것인지
chdir = '/srv/instagram/app'
bind = 'unix:/run/instagram.sock'
accesslog = '/var/log/gunicorn/instagram-access.log'
errorlog = '/var/log/gunicorn/instagram-error.log'
capture_output = True
