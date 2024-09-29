# Importing libraries
import imaplib, email
 
user = 'refoteam0@gmail.com'
password = 'phtn hgeb slsn wxdu'
imap_url = 'imap.gmail.com'
 
# Function to get email content part i.e its body part
def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)
 
# Function to search for a key value pair 
def search(key, value, con): 
    result, data = con.search(None, key, '"{}"'.format(value))
    return data
 
# Function to get the list of emails under this label
def get_emails(result_bytes):
    msgs = [] # all the email data are pushed inside an array
    for num in result_bytes[0].split():
        typ, data = con.fetch(num, '(RFC822)')
        msgs.append(data)
 
    return msgs

con = imaplib.IMAP4_SSL(imap_url) 
con.login(user, password) 
con.select('Inbox') 
msgs = get_emails(search('FROM', 'no-reply@sms-forwarder.com', con))
list=[]
c=0
fc=-1
while fc>-6:
    msgg=msgs[fc][0][1]
    l= msgg.split()
    for i in l:
        f=i.decode('utf-8')
        if f[0]=='(' and f[1].isdigit():
            c=0
        if c==1:
            list.append(f)
        if f=='br/>Message:':
            c=1
    amount = list[1]
    if amount[0].isdigit():
        print(amount)
    l=[]
    list=[]
    fc-=1


