import clipboard

#----------------------------------------------------------------------
if __name__ == "__main__":

    text = clipboard.paste()  # text will have the content of clipboard
    print (text)

    filename = "z:\\temp2.txt"

    with open(filename, 'w', encoding = "utf8") as the_file:
        the_file.write(text)

    with open(filename, 'r+', encoding = "utf8") as fd:
        lines = fd.readlines()
        fd.seek(0)
        fd.writelines(line for line in lines if line.strip())
        fd.truncate()