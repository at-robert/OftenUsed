import clipboard
import re
import codecs

#----------------------------------------------------------------------
def remove_str_from_file_(file_r_, file_w_,pattern_):

    with open(file_r_ , 'r', encoding = "utf8") as f:
        for line in f:
            str = line
            str = re.sub(pattern_, '', str)

                
            # print (str)

            with open(file_w_, 'a', encoding = "utf8") as the_file:
                the_file.write(str)

#----------------------------------------------------------------------
def grep_from_file(file_r_, file_w_,pattern_):

    with open(file_r_ , 'r', encoding = "utf8") as f:
        for line in f:
            
            if re.search(pattern_, line):
                print(line)
                with open(file_w_, 'a', encoding = "utf8") as the_file:
                    the_file.write(line)

#----------------------------------------------------------------------
def clear_file_(file_):
    text_file = open(file_, "w", encoding = "utf8")
    text_file.write('')
    text_file.close()


#----------------------------------------------------------------------
def remove_empty_line(file_):
    with open(file_, 'r+', encoding = "utf8") as fd:
        lines = fd.readlines()
        fd.seek(0)
        fd.writelines(line for line in lines if line.strip())
        fd.truncate()

#----------------------------------------------------------------------
if __name__ == "__main__":

    text = clipboard.paste()  # text will have the content of clipboard
    print (text)

    filename2 = "z:\\temp2.txt"
    filename3 = "z:\\temp3.txt"

    # To write clipboard content into the filename2
    with open(filename3, 'w', encoding = "utf8") as the_file:
        the_file.write(text)
    
    remove_empty_line(filename3)
    clear_file_(filename2)

    grep_from_file(filename3,filename2,"結論")

    clear_file_(filename3)
    remove_str_from_file_(filename2,filename3,'"結論：')

    with open(filename3,'r',encoding = "utf8") as f:
        StrA = "".join(f)
        clipboard.copy(StrA)

