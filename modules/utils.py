color = {
    'white':    "\033[1;37m",
    'yellow':   "\033[1;33m",
    'green':    "\033[1;32m",
    'blue':     "\033[1;34m",
    'cyan':     "\033[1;36m",
    'red':      "\033[1;31m",
    'magenta':  "\033[1;35m",
    'black':      "\033[1;30m",
    'darkwhite':  "\033[0;37m",
    'darkyellow': "\033[0;33m",
    'darkgreen':  "\033[0;32m",
    'darkblue':   "\033[0;34m",
    'darkcyan':   "\033[0;36m",
    'darkred':    "\033[0;31m",
    'darkmagenta':"\033[0;35m",
    'darkblack':  "\033[0;30m",
    'off':        "\033[0;0m"
}

def error(message):
    print("%s%s%s" %(color['red'], message, color['off']))

def message(message):
    print("%s%s%s" %(color['darkred'], message, color['off']))
    
def notify(message):
    print("%s%s%s" %(color['green'], message, color['off']))
    
def warning(message):
    return print("%s%s%s" %(color['darkmagenta'], message, color['off']))

def debug(message):
    return print("%s%s%s" %(color['darkgreen'], message, color['off']))
