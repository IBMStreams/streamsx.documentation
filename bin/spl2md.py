import os
import sys
import textwrap

def generateIndex( indexFile,  title,  url):

    if not os.path.exists(os.path.dirname(indexFile)):
        os.makedirs(os.path.dirname(indexFile))

    with open(indexFile, "a+") as f:
        title = textwrap.wrap(title, 28)
        f.write("<li><a href=\"" + url + "\">" + title[0] + "</a></li>\n")

def nextUrl(url):
    return "<a class=\"button\" href=\"" + url + "\">"  + " > </a>"

def prevUrl(url):
    return "<a class=\"button\" href=\"" + url + "\">"  + " < </a>"

def writeButtons(f, prev, next):
    f.write("<div class=\"sampleNav\">")
    if len(prev) > 0:
        prevButton = prevUrl(prev)
        f.write(prevButton)

    if len(next) > 0:
        nextButton = nextUrl(next)
        f.write(nextButton + "\n")
    f.write("</div>\n\n")

def splToMd(splFile, mdFile, title, prev, next):

    with open(splFile, "r") as splF:
        content = splF.read()

    if not os.path.exists(os.path.dirname(mdFile)):
        os.makedirs(os.path.dirname(mdFile))

    with open(mdFile, "w+") as f:
        f.write("---\n")
        f.write("layout: samples\n")
        f.write("title: " + title + "\n")
        f.write("---\n\n")
        f.write("## " + title + "\n\n")

        writeButtons(f, prev, next)

        f.write("~~~~~~\n")
        f.write(content + "\n")
        f.write("~~~~~~\n\n")

        writeButtons(f, prev, next)

        print "Generated: " + mdFile

path = "/Users/chanskw/git/splexamples/SPL-Examples-For-Beginners"
outPath = "/Users/chanskw/git/streamsx.documentation/samples/spl-for-beginner"
spl = ".spl"
md = ".md"
index = os.path.join("/Users/chanskw/git/streamsx.documentation/_includes" + "/sampleIndex.html")

if (os.path.exists(index)):
    os.remove(index)

indexList = []

for root, subdirs, files in os.walk(path):
    for oneFile in files:
        absPath = os.path.join(root, oneFile)
        relOutPath = os.path.relpath(absPath, path)

        splitted = relOutPath.split("/")
        sampleName = splitted[0]

        absOutPath = os.path.join(outPath, sampleName + md)

        outPathLen = len(absOutPath)
        end = outPathLen-len(spl) + 1
        absOutPath = absOutPath[0:end]
        absOutPath = absOutPath + md

        if absPath.endswith(spl):
            htmlPath = "../" + sampleName + "_" + oneFile + "/"
            generateIndex(index, sampleName, htmlPath)
            indexList.append(htmlPath)

i = 0
max = len(indexList)
print max

for root, subdirs, files in os.walk(path):
    for oneFile in files:
        absPath = os.path.join(root, oneFile)
        relOutPath = os.path.relpath(absPath, path)

        splitted = relOutPath.split("/")
        sampleName = splitted[0]

        absOutPath = os.path.join(outPath, sampleName + "_" + oneFile + md)

        outPathLen = len(absOutPath)
        end = outPathLen-len(spl) + 1
        absOutPath = absOutPath[0:end]
        absOutPath = absOutPath + md

        if absPath.endswith(spl):

            print i

            if i > 0:
                prev = indexList[i-1]
            else:
                prev=""

            if i < max-1:
                next = indexList[i+1]
            else:
                next=""

            splToMd(absPath, absOutPath, sampleName, prev, next)

            i=i+1
