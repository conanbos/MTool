import os
import xml.sax
###TODO InputOutput interface, various xml formats
def output_file(filename, type, content):
    '''
    output contents to file
    :param filename:
    :param type: 0:w+ rewrite mode, 1:a+ append mode
    :param content:
    :return:
    '''
    if (type == 0):
        with open(filename, 'w+', 1) as f:
            f.write(content + os.linesep)
    if (type == 1):
        with open(filename, 'a+', 1) as f:
            f.write(content + os.linesep)
    try:
        f.close()
    except:
        pass

def IO_output_xml(filename, type, content=[]):
    print("save xml")
    return 0






