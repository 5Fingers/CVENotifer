__version__ = '1.0'
__author__ = '5Fingers'
__license__ = 'GNU'

import configparser
import os
import time
import requests as requests
import smtplib


class CVENotifier:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.cve_data = {}

    def extract_data(self):
        res = requests.get(self.config['general']['url'])
        try:
            self.cve_data = res.json()['data']
        except KeyError:
            data = None

    def build_html_page(self):
        content = ''
        for cve_item in self.cve_data:
            content += f"<table class ='table table-bordered tb'>"
            content += f"<tbody>"
            content += '<tr>'
            content += f"<th rowspan='3' class='titleColumn'>{cve_item['cve']}</th>"
            content += f"<td class='dotted'><b>Assigner:</b> {cve_item['assigner']} <br /> " \
                       f"<b>Severity:</b> {cve_item['cvssv3_base_severity']} <br /> " \
                       f"<b>PublishedDate:</b> {cve_item['publishedDate']} <br /> " \
                       f"<b>LastModifiedDate:</b> {cve_item['lastModifiedDate']} </td>"
            content += f"<td class='dotted'><b>Description:</b> <br /> {cve_item['description']} </td>"
            if len(cve_item['github_repos']) > 0:
                content += f"<td class='dotted'><b>GitHub Repos:</b> <br />"
                for repo in cve_item['github_repos']:
                    content += f"<b>Repo Title:</b> <br /> {repo['description']} <br /> " \
                               f"<a href='{repo['url']}'>{repo['url']}</a>  <br />"
                content += "</td>"
            content += "</tr>"
            content += "</tbody>"
            content += "</table>"

        with open(self.config['general']['html_template_filename'], 'r') as file:
            filedata = file.read()

        filedata = filedata.replace('[placeholder]', content)

        with open(os.getcwd() + '/output/' + self.config['general']['html_template_filename'] +
                  time.strftime("%Y%m%d-%H%M%S") + '.html', 'w') as file:
            file.write(filedata)

        self.notify(filedata)

    def notify(self, email_content):
        server = smtplib.SMTP(self.config['mail_det']['smtp_server'], self.config['mail_det']['smtp_server_port'])
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(self.config['mail_det']['smtp_username'], self.config['mail_det']['smtp_password'])
        server.sendmail(self.config['mail_det']['email_sender'], self.config['mail_det']['email_recipients'], email_content)
        server.quit()


if __name__ == '__main__':
    cve = CVENotifier()
    cve.extract_data()
    cve.build_html_page()
    print('The notification was sent to the recipients successfully!')
