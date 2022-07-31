# CVE-Notifer

## Introduction
Every person who works as Threat Intelligence knows how important it is to stay updated on everything that is happening around us.
In a world where there are a lot of updates and changes, it's hard to remember to check what's new on all the sites that can provide us with intelligence while researching
This tool extracts the information from the https://cvetrends.com and sends it by email - by push!
Personally, I set a schedule for myself that every Monday I receive an email with the latest updates - And that's how I start the week

## Configuration
This tool have a config file which allow you to set your own email details and run this tool without making any changes.
```python
[general]
url = https://cvetrends.com/api/cves/order-by-tweets-7days
html_template_filename = notifier-template.html

[mail_det]
subject = CVE-Trends
recipients = pat
smtp_server = smtp-mail.outlook.com
smtp_server_port = 587
smtp_username = username
smtp_password = password
email_sender = sender
email_recipients = recipients
```

## Screenshots
![Screen Shot 2022-07-31 at 21 07 44](https://user-images.githubusercontent.com/6413401/182042443-d00c50f7-d98c-4b34-b970-da821cef32de.png)


## License
GNU
