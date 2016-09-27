#!/usr/bin/python
import sys
import subprocess
import email.utils

# cmd = '/home/woodsman/work/Kernel/linux-next/scripts/get_maintainer.pl'
cmd = 'scripts/get_maintainer.pl'
cmdMutt = 'mutt'

def lineParse(fullLine):
    result = email.utils.parseaddr(fullLine)
    # parseaddr returns two string which are name and e-mail address
    # I need to get only e-mail address for mutt
    return result[1]

def getMaintainer(patchName):
    args = [cmd, patchName]
    lists = []
    p = subprocess.Popen(args, stdout=subprocess.PIPE,\
                         stderr=subprocess.STDOUT)

    while True:
        out = p.stdout.readline()
        if out == '' and p.poll() != None:
                break
        lists.append(lineParse(out))

    # adds janitors mailing list address for review
    lists.append("kernel-janitors@vger.kernel.org");
    return lists

def getSubjectFromPatchFile(patchFile):
    subject = ""
    findSub = False

    for line in open(patchFile ,'r'):

        if (not findSub) and (line.find("Subject") > -1):
            # remove "Subject:" string and "\n"
            subject = line[9:-1]
            findSub = True
            continue

        if findSub:
            if len(line) > 0:
                    subject += line
            return subject[:-1]
    return ""


def setAndSendMainWithMutt(maintainerList, patchName):
    # first element is MAINTAILER for "TO"
    # rest of e-mail list are "CC"
    Subject = getSubjectFromPatchFile(patchName)
    args = [cmdMutt, '-i', patchName, maintainerList[0], '-s', Subject, '-c']
    del maintainerList[0]

    args.append(', '.join(maintainerList))

    p = subprocess.Popen(args)
    # wait for mutt
    p.communicate()

if __name__ == "__main__":
    # get an argument from shell
    # first parameter is a patch file made by me.
    # this script get only one parameter.
    parmCount = len(sys.argv)

    if parmCount == 1 or parmCount > 3:
            print "Usage: %s <patch file>"% sys.argv[0]
            exit(1)

    maintainerList = getMaintainer(sys.argv[1])
    setAndSendMainWithMutt(maintainerList, sys.argv[1])
