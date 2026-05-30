"""Meat Engine Word Wrap code

Modular word wrapping routine"""



def fixedWidthFontWidthFunc(string):
    """ to lay out text using a fixed width font, measure the text
    width in characters.
    """
    return len(string)

def wrap(string, paragraphWidth, strLenFunc=fixedWidthFontWidthFunc, insertParagraphBreak=True):
    lines=[]
    paragraphs=string.split("\n")

    for p in paragraphs:
        # split on any whitespace, and treat it all identically - I
        # could be smarter about tabs, perhaps.
        words=p.split()
        workingString=""
        while words:
            newStr=workingString
            if newStr:
                newStr+=" "
                oneWord=False
            else:
                oneWord=True
            newStr+=words[0]

            if strLenFunc(newStr)>paragraphWidth and not oneWord:
                #too big - emit the previous working string
                lines.append(workingString)
                workingString=""
            else:
                workingString=newStr
                words=words[1:]
        if workingString:
            lines.append(workingString)
        if insertParagraphBreak:
            lines.append("")
    return lines


def unwrap(string):
    """reverses the wrap function - handy for reformatting text that's
    wrapped in an editor"""
    paragraphs=[]

    lines=[x.strip() for x in string.split("\n")]

    workingParagraph=""
    for s in lines:
        if (not s) and workingParagraph:
            paragraphs.append(workingParagraph)
            workingParagraph=""
        if workingParagraph:
            workingParagraph+=" "
        workingParagraph+=s

    return '\n'.join(paragraphs)
        
        


if __name__=="__main__":

    text="""
Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Pellentesque
vitae lectus. Cras mattis enim. Mauris ac nisl eu lorem condimentum
convallis. Nunc vestibulum est. Curabitur hendrerit egestas
massa. Praesent varius, risus ac interdum condimentum, felis mi
tincidunt elit, nec hendrerit lectus nisi sit amet est. In
diam. Suspendisse aliquet hendrerit lacus. Integer quis magna ut arcu
pulvinar dignissim. Suspendisse potenti. Mauris congue augue id
elit. Class aptent taciti sociosqu ad litora torquent per conubia
nostra, per inceptos hymenaeos. Ut interdum mollis felis. Suspendisse
pharetra lorem nec mi. Nulla blandit. Duis congue.

Donec vel orci a nisi malesuada porta. Fusce nonummy interdum
nunc. Sed venenatis cursus ligula. Proin rhoncus velit sed
ligula. Cras sollicitudin diam id mi. In ligula. Morbi turpis pede,
euismod id, dictum et, aliquet sed, felis. Praesent metus. Nunc
dapibus condimentum libero. Nulla ac sapien vel neque tincidunt
lacinia. Phasellus ipsum. Nunc eu ipsum. Mauris erat felis, vulputate
ut, tempus nec, pulvinar et, purus. Nunc non mi. Vivamus dignissim
neque quis dui.

Pellentesque id neque. Vivamus malesuada neque sit amet velit. Fusce
ut odio. Etiam cursus, turpis at aliquam viverra, elit lectus faucibus
sapien, sit amet lobortis justo urna sed ligula. Nunc pharetra gravida
dolor. Class aptent taciti sociosqu ad litora torquent per conubia
nostra, per inceptos hymenaeos. Aliquam erat volutpat. Ut malesuada
mauris. Praesent mattis metus tempor lectus. Suspendisse venenatis
placerat justo. Nam tristique, risus ac lacinia ultricies, nisl odio
facilisis orci, eu commodo velit magna ut sem. Sed sollicitudin
malesuada nunc. Cras non massa. Fusce a enim sed odio tincidunt
tempus. Sed blandit est ac sapien.

Vestibulum ante ipsum primis in faucibus orci luctus et ultrices
posuere cubilia Curae; Vestibulum molestie, eros at placerat mattis,
diam ipsum scelerisque massa, vitae molestie ipsum magna id
magna. Pellentesque habitant morbi tristique senectus et netus et
malesuada fames ac turpis egestas. Phasellus metus mi, commodo auctor,
sollicitudin eget, placerat nec, urna. Cras enim lorem, congue eget,
ornare quis, bibendum vitae, magna. Integer varius. Pellentesque
auctor, metus a dictum viverra, purus magna placerat purus, nec
volutpat est lorem a tellus. Pellentesque habitant morbi tristique
senectus et netus et malesuada fames ac turpis egestas. Sed vehicula
posuere neque. Nam commodo rhoncus diam. Vestibulum ornare. Nunc metus
erat, egestas sed, semper at, vestibulum vitae, tellus. Integer augue
felis, consequat vel, tincidunt quis, accumsan sit amet, odio. Sed
mollis, leo sit amet sagittis imperdiet, justo risus dictum orci, a
dapibus lorem pede laoreet sem. Vivamus pretium. Mauris vel dolor a
ligula congue convallis. Proin mauris metus, luctus sed, venenatis at,
hendrerit nec, augue. Nullam massa magna, feugiat ut, ornare in,
aliquet non, mauris.

Nulla facilisi. Cras at libero. Cras mi. Maecenas purus. Donec at
augue. Nulla aliquam. Mauris id risus luctus diam ornare
ornare. Praesent commodo porttitor leo. In porttitor sollicitudin
dolor. Proin eleifend nulla at risus. Nulla commodo nisi. Integer ut
enim.
"""

    unwrappedText=unwrap(text)
    print unwrappedText

    for width in range(5,65,5):
        print "WORD WRAP TEST (%d)"%width
        print "="*40
        
        wrappedText=wrap(unwrappedText, width)
        print '\n'.join(wrappedText)

        print
        
        



        
        
