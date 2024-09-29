from imap_tools import MailBox

user = 'refoteam0@gmail.com'
password = 'phtn hgeb slsn wxdu'
with MailBox('imap.gmail.com').login(user,password,"Inbox") as mb:
    for msg in mb.fetch(limit=1,reverse=True,criteria='Seen'):
        print(msg.subject,msg.date,msg.flags,msg.text)