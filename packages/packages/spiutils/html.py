def tag(name, content, nl):
    return '<' + name + '>' + content + '</' + name + '>' + (nl and '\n')
