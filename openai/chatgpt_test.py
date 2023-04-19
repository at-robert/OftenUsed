
import os
import openai
import re
import platform


FILE_PATH_OPENAI_CERT=r"D:\work_platform\CERT\openai_cert"

FILE_PATH_MACOS_OPENAI_CERT= 'Documents/CERT/openai_cert'


#----------------------------------------------------------------------
def search_auth_file(folder, cert_data_):
    # print ("Target Path = {}".format(folder))
    c = re.compile(r'\[cert\]', re.IGNORECASE)

    fp = open(folder,"r")
    zops = fp.readlines()
    for lineStr in zops:
        if(c.match(lineStr)):
            lineStr = lineStr.strip()
            cert_data_.append(re.sub(c,r'',lineStr))


#----------------------------------------------------------------------
if __name__ == "__main__":


    pwd = os.path.expanduser('~') + '/'
    cert_data = []

    if platform.system() == 'Darwin':
        print("It's Mac OS system!!")
        path_ = pwd + FILE_PATH_MACOS_OPENAI_CERT
    else:
        path_ = FILE_PATH_OPENAI_CERT

    search_auth_file(path_,cert_data)
    print(cert_data[0])

    openai.api_key = cert_data[0]
    message = ''

    while message != 'quit':
        # Read a message from the user
        message = input("You: ")

        if message == 'quit':
            break

        # Use GPT-3 to generate a response
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt = message,
            max_tokens=2048,
            temperature=0.9,
        )
        print("Bot: ", response.choices[0].text)