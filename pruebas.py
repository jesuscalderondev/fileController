def getMails(mails:str):
    return [mails.split(", ")]


print(*getMails("jesus@gmail.com, hola@g.com"))