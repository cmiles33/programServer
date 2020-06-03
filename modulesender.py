import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
import re
import sqlmethods

# The language modules will be the same Practically, then can be wraped in this one module
# What we need to do
# Redo the server code
# Finish the module code
def makeFrench(informationTup):
    firstName = informationTup[0]
    startTime = informationTup[2]
    endTime = informationTup[3]
    payloadNumber = informationTup[4]
    subject = "Hey {} here is your French payload number {}!".format(firstName, payloadNumber)

    theTing = open('emails/payloads/french.html')
    myHtmlFile = BeautifulSoup(theTing,'html.parser')
    theTing.close()
    myHtmlFile.patronname.append(firstName)
    myHtmlFile.starttime.append(startTime)
    myHtmlFile.endtime.append(endTime)
    readOut = open('payloads/french/payload{}.txt'.format(payloadNumber),encoding='utf-8')
    counter = 0
    for lines in readOut:
        if counter == 0:
            myHtmlFile.payload0.append(lines)
        if counter == 1:
            myHtmlFile.payload1.append(lines)
        if counter == 2:
            myHtmlFile.payload2.append(lines)
        if counter == 3:
            myHtmlFile.payload3.append(lines)
        if counter == 4:
            myHtmlFile.payload4.append(lines)
        if counter == 5:
            myHtmlFile.payload5.append(lines)
        if counter == 6:
            myHtmlFile.payload6.append(lines)
        if counter == 7:
            myHtmlFile.payload7.append(lines)
        counter +=1
    print(myHtmlFile.get_text())
    return subject, myHtmlFile

def makeSpanish(informationTup):
    firstName = informationTup[0]
    startTime = informationTup[2]
    endTime = informationTup[3]
    payloadNumber = informationTup[4]
    subject = "Hey {} here is your French payload number {}!".format(firstName, payloadNumber)
    pageSend = open('emails/payloads/advanceSpanish.htm','r')
    tempFile = open('emails/payloads/spanishTemp.html','w')

    tempFile.writelines(pageSend.readlines())
    payloadRead = open('payloads/spanishAdv/spanPayloads{}.txt'.format(payloadNumber),encoding='utf-8')
    pageSend.close()
    for lines in payloadRead.readlines():
        tempFile.write('''<p class=MsoNormal style='line-height:150%'><span style='font-size:14.0pt;
line-height:150%;font-family:"Garamond","serif"'>{}</span></p>'''.format(lines))
    payloadRead.close()
    tempFile.write('''<p class=MsoNormal><span style='font-size:14.0pt;line-height:200%;font-family:
"Garamond","serif"'>&nbsp;</span></p> ''')
    tempFile.write('''</div> ''')
    tempFile.write('''</body> ''')
    tempFile.write('''</html> ''')
    tempFile.close()
    tempFile = open('emails/payloads/spanishTemp.html', 'r')
    htmlObject = BeautifulSoup(tempFile, 'html.parser')
    tempFile.close()
    htmlObject.firstname.append(firstName)
    htmlObject.starttime.append(startTime)
    htmlObject.endtime.append(endTime)
    print(htmlObject.get_text())
    return subject, htmlObject

def makeWorkout(name):
    print("We gone work out doh")



def sendEmail(customerID):
    # Get config file information:
    emailInfoDic = {}
    configOpen = open('config.txt','r')
    for lines in configOpen.readlines():
        (key,val) = lines.split()
        emailInfoDic.update({key : val})
    configOpen.close()
    sender_email = emailInfoDic['email']
    password = emailInfoDic['password']
    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    # Make the Quary for customer information
    myQuary = sqlmethods.mySQLMethods()
    myQuary.cursor.execute("select first_name, email, start, end, payload, module from contacts where id = '{}';".format(customerID))
    contactTup = myQuary.cursor.fetchall()
    contactTup = contactTup[0]
    receiver = contactTup[1]
    message["To"] = receiver
    payloadNum = contactTup[4]
    # Create the correct payload
    if contactTup[5] == 'french':

        subject ,payload = makeFrench(contactTup)

    elif contactTup[5] == 'spanish':

        subject, payload = makeSpanish(contactTup)

    else:

        print("No module found, skipping customer")

        return False

    # Atach the payloads to the email
    text = payload.get_text()
    part1 = MIMEText(text,"plain")
    part2 = MIMEText(payload,"html")
    message["Subject"] = subject
    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver, message.as_string()
        )

    payloadNum += 1
    myQuary.setPayload(customerID,payloadNum)
    myQuary.closeConnections()