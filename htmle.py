#!/usr/bin/env python

import os
import sys
import getopt
from htmlentitydefs import name2codepoint

usageString = 'appname ...'
helpString = """
oh hi imma help string
"""

class Application:
    def run(self, optlist, args):

        self.options = {}
        self.options['pager'] = False
        self.options['columns'] = 4
        self.options['outfile'] = sys.stdout
        
        rows, columns = os.popen('stty size', 'r').read().split()

        for o, i in optlist:
            if o in ('-h', '--help'):
                sys.stderr.write(usageString)
                sys.stderr.write(helpString)
                sys.exit(1)

            elif o in ('-p', '--pager'):
                self.options['pager'] = True

            elif o in ('-c', '--columns'):
                try:
                    self.options['columns'] = int(i)
                except ValueError:
                    sys.stderr.write('Warning: Invalid column value %s. Setting to 4\n', i)

                if self.options['columns'] == 0:
                    sys.stderr.write('Error: Invalid column value 0. Exiting...\n')
                    sys.exit(1)

            elif o in ('-o', '--output'):
                outfile = open(i, 'w')
                self.options['outfile'] = outfile
                

                    #{ 'name': 'ASCII', 
                    # 'r' : range(33, 127)},
        ranges = [
                   { 'name': 'ISO 8859-1', 
                     'r' : range(160, 173) + range(174, 256)},
                   
                   { 'name': 'Latin Extended-B', 
                     'r' : range(402, 403)},

                   { 'name': 'Greek', 
                     'r' : range(913, 983)},
                                      
                   { 'name': 'General Punctuation', 
                     'r' : [8226, 8230, 8242, 8243, 8254, 8260]},
                   
                   { 'name': 'Letterlike Symbols', 
                     'r' : [8472, 8465, 8476, 8482, 8501]},

                   { 'name': 'Arrows', 
                     'r' : [8592, 8593, 8594, 8595, 8596, 8629, 8656, 8657, 8658, 8659, 8660]},

                   { 'name': 'Mathematical Operators', 
                     'r' : [8704, 8706, 8707, 8709, 8711, 8712, 8713, 8715, 8719, 8721, 8722,
                            8727, 8730, 8733, 8734, 8736, 8743, 8744, 8745, 8746, 8747, 8756,
                            8764, 8773, 8776, 8800, 8801, 8804, 8805, 8834, 8835, 8836, 8838,
                            8838, 8839, 8853, 8855, 8869, 8901]},
                   
                   { 'name': 'Miscellaneous Technical', 
                     'r' : [8968, 8969, 8970, 8971, 9001, 9002]},
                   
                   { 'name': 'Geometric Shapes', 
                     'r' : [9674]},
                   
                   { 'name': 'Miscellaneous Symbols', 
                     'r' : [9824, 9827, 9829, 9830]},

                   { 'name': 'C0 Controls and Basic Latin', 
                     'r' : [34, 38, 60, 62]},
                   
                   { 'name': 'Latin Extended-A', 
                     'r' : [338, 339, 352, 353, 376]},

                   { 'name': 'Spacing Modifer Letters', 
                     'r' : [710, 732]},
                   
                   { 'name': 'General Punctuation', 
                     'r' : [8194, 8195, 8201, 8204, 8205, 8206, 8207,
                            8211, 8212, 8216, 8217, 8218, 8220, 8221, 8222, 8224, 8225, 8240, 8249,
                            8250]},

                   { 'name': 'Currency', 
                     'r' : [8364]}
                   

                   #, range(8704, 9999)
                  ]


        codepointDict = self.codepoint2name()

        if self.options['outfile'] == sys.stdout:
            sep = unichr(27) + '[32m|' + unichr(27) + '[0m'
        else:
            sep = '|'

        logList = []

        for rangeDict in ranges:
            count = 0;
            bufList = []
            r = rangeDict['r']

            logList.append('## %s' % rangeDict['name'])
            for i in r:
                if codepointDict.has_key(i):
                    codepoint = codepointDict[i]
                else:
                    codepoint = ' ' * 8
                
                buf = '%4d %-8s %s' % (i, codepoint, unichr(i))
                
                bufList.append(buf)
                count = count + 1
                if (count % self.options['columns']) == 0:
                    logList.append(sep.join(bufList))
                    #sys.stdout.write(sep.join(bufList))
                    #sys.stdout.write('\n')
                    bufList = []
                    count = 0
            else:
                logList.append(sep.join(bufList))
                #logList.append('\n')
                #sys.stdout.write(sep.join(bufList))
                #sys.stdout.write('\n')
                count = 0

        count = 0
        for line in logList:
                
            self.options['outfile'].write(line.encode('utf-8'))
            self.options['outfile'].write('\n')
            count = count + 1


            if self.options['pager']:
                if (count % (int(rows)-2)) == 0:
                    z = raw_input('Press enter to continue:')

                    if z in ('q', 'Q'):
                        sys.exit(0)
                        count = 0
                
        if self.options['outfile'] != sys.stdout:
            self.options['outfile'].close()


    def codepoint2name(self):
        result = {}
        for key in name2codepoint.keys():
            result[name2codepoint[key]] = key

        return result
            
                
if __name__ == '__main__':

    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'hpc:o:',
                                      ('help'
                                       , 'pager'
                                       , 'outfile='
                                       , 'columns='))
    except getopt.error, msg:
        sys.stderr.write(msg + '\n')
        sys.stderr.write(usageString)
        sys.exit(1)

    
    app = Application()
    app.run(optlist, args)
    
    
    
    
    


