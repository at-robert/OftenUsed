
import re

#----------------------------------------------------------------------
def check_file_(file_r_, file_w_):

    with open(file_r_ , 'r') as f:
        for line in f:
            str = line
            str = re.sub('Tony Ho \(何哲嘉\)	回覆: 104自訂配對人選【.*】', ' ', str)

            if(str == line):
                str = re.sub('Austin Tseng \(曾炅文\)	回覆: 104自訂配對人選【.*】', ' ', str)

            if(str == line):
                str = re.sub('Austin Tseng \(曾炅文\)	Re: 104自訂配對人選【.*】', ' ', str)

            if(str == line):
                str = re.sub('Austin Tseng \(曾炅文\)	Re: 104應徵履歷【.*】', ' ', str)
                
            # print (str)

            with open(file_w_, 'a') as the_file:
                the_file.write(str)

#----------------------------------------------------------------------
if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print ('no argument; Usage: python srt_check.py IN_PATH')
    #     sys.exit()
    
    # target_path = str(sys.argv[1])
    # print ("Target Path = {}".format(target_path))
    # search_file(target_path)



    # str = 'aaa@gmail.com bbb@hotmail.com ccc@apple.com'
    # str = 'Tony Ho (何哲嘉)	回覆: 104自訂配對人選【韌體資深工程師/主任工程師】謝承佑(桃園市中壢區)	(週一) 上午 10:41	97 KB'
    # str = re.sub('Tony Ho \(何哲嘉\)	回覆: 104自訂配對人選【.*】', ' ', str)
    # print(str)

    # clear file
    text_file = open("temp3.txt", "w")
    text_file.write('')
    text_file.close()


    check_file_("temp2.txt","temp3.txt")