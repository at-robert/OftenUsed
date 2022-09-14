import clipboard
import re
import codecs


#----------------------------------------------------------------------
def check_file_(file_r_, file_w_):

    out_ = []
    with open(file_r_ , 'r', encoding = "utf8") as f:
        for line in f:
            str = line
            str = re.sub('Tony Ho \(何哲嘉\)	回覆: 104自訂配對人選【.*】', ' ', str)

            if(str == line):
                str = re.sub('Austin Tseng \(曾炅文\)	回覆: 104自訂配對人選【.*】', ' ', str)

            if(str == line):
                str = re.sub('Austin Tseng \(曾炅文\)	Re: 104自訂配對人選【.*】', ' ', str)

            if(str == line):
                str = re.sub('Austin Tseng \(曾炅文\)	Re: 104應徵履歷【.*】', ' ', str)

            if(str == line):
                str = re.sub('^.* 104自訂配對人選【.*】', ' ', str)

            if(str == line):
                str = re.sub('^.*	RE: 104應徵履歷【.*】', ' ', str)

            if(str == line):
                str = re.sub('104配對人選	104自訂配對人選【.*】','',str)
                
            # print (str)
            str_a = str.split('(')
            str = str_a[0].strip() + '\n'
            out_.append(str)

    out_.pop(0)
    StrA = "".join(out_)
    clipboard.copy(StrA)

    with open(file_w_, 'w', encoding = "utf8") as the_file:
        the_file.write(StrA)

#----------------------------------------------------------------------
if __name__ == "__main__":

    text = clipboard.paste()  # text will have the content of clipboard
    print (text)

    filename2 = "D:\\work_platform\\temp2_1.txt"
    filename3 = "D:\\work_platform\\temp3_1.txt"

    with open(filename2, 'w', encoding = "utf8") as the_file:
        the_file.write(text)

    with open(filename2, 'r+', encoding = "utf8") as fd:
        lines = fd.readlines()
        fd.seek(0)
        fd.writelines(line for line in lines if line.strip())
        fd.truncate()

    text_file = open(filename3, "w", encoding = "utf8")
    text_file.write('')
    text_file.close()

    check_file_(filename2,filename3)
