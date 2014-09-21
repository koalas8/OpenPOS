#-*-coding=utf-8-*-
import random
import smtplib
import ConfigParser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#
# def get_config(section, option):
#     ''' 从配置文件中读取配置 '''
#     cf = ConfigParser.ConfigParser()
#     cf.read('/data/www/angcard/app/config.cfg')
#     return cf.get(section=section, option=option)

class Downloader:
    '''
    >>> rpt_data = [
            [column_1, column_2, column_3, ..., column_n],
            [column_1, column_2, column_3, ..., column_n],
            [column_1, column_2, column_3, ..., column_n],
            ...
            [column_1, column_2, column_3, ..., column_n],
        ]
    >>> downloader = Downloader()
    >>> downloader.create_file(rpt_data).download()
    '''
    
    def download(self):
        web.header('Content-type', 'application/x-octet-stream')
        web.header('Content-Disposition', 'attachment;filename="%s"' % self._report_name)
        f = open(self._report_file, 'rb')
        return f

    def create_file(self, rpt_data=[], rpt_name=''):
        row_index = 0  # 行序号
        sheet_index = 1  # 工作表序号,当行序号等于65536时需要将其+1
        wb = xlwt.Workbook()
        ws = wb.add_sheet('sheet%s' % sheet_index)

        
        for row in rpt_data:
            column_index = 0  

            for cell in row:
                ws.write(row_index, column_index, cell)
                print 'r->', row_index, 'column->', column_index, 'cell->', cell
                column_index += 1
            row_index += 1

            if row_index % 65536 == 0:  # 达到Excel表行数的极限时添加新表
                sheet_index += 1
                row_index = 1
                ws = wb.add_sheet('sheet%s' % sheet_index)

        f = 'report_files/%s.xls' % str(uuid.uuid4())
        wb.save(f)

        self._report_file = f
        if not rpt_name:
            self._report_name = f
        else:
            self._report_name = rpt_name
        return self


class MyEmail(object):
    def send_email(self, _from, password, to, subject, content, attrs=[]):
        msg = MIMEMultipart()
        msg['Subject'] = subject            
        msg['From'] = _from      
        msg['To'] = to

        html = MIMEText(content.encode('utf-8'), 'html', 'utf-8')
        msg.attach(html)
        try:    
            smtp = smtplib.SMTP()
            smtp.connect(u'smtp.ym.163.com')
            smtp.login(_from, password)      
            smtp.sendmail(msg['From'], msg['To'], msg.as_string())
            return True
        except Exception, e:
            print e.message
            return False
        else:
            smtp.quit()


