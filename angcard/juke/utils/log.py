#encoding=utf-8

from datetime import datetime

def write2file(log_file, log_content):
    now = datetime.now().strftime('%Y-%m-%d')
    f = open(log_file, 'ab+')
    f.writelines('%s\t%s\n' % (now, log_content))
    f.close()