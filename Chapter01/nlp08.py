from string import Template
 
def formatText(x, y, z):
    return "{hour}時の{target}は{value}".format(hour=x, target=y, value=z)
 
def formatText2(x, y, z):
    s = Template('$hour時の$targetは$value')
    return s.substitute(hour=x, target=y, value=z)
 
def formatText3(x, y, z):
    return '%s時の%sは%s' % (x, y, z)
 
def main():
    x = 12
    y = "気温"
    z = 22.4
    print(formatText(x, y, z))
    print(formatText2(x, y, z))
    print(formatText3(x, y, z))
 
main()
