#!/usr/bin/env python
#
# Copyright 2011 Yummy Melon Software LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import getopt
from htmlentitydefs import name2codepoint
import ConfigParser

class Henty:
    def __init__(self):
        self.columnTemplate = '%4d %-8s %s'
        
        self.options = {}
        self.options['pager'] = False
        self.options['outfile'] = sys.stdout
        self.options['sep'] = '|'
        self.options['color'] = False

        self.colorConfig = { 'symbolColor': 'yellow',
                             'symbolBackground': 'default',
                             'separatorColor': 'green',
                             'separatorBackground': 'default'}

        configPath = os.path.join(os.environ['HOME'],
                                  '.henty')
        if os.path.exists(configPath):
            self.options['color'] = True
            self.config = ConfigParser.ConfigParser()
            self.config.read(configPath)
            self.colorConfig = {}
            try:
                self.colorConfig['symbolColor'] = self.config.get('Colors', 'symbolColor')
            except ConfigParser.NoOptionError:
                pass

            try:
                self.colorConfig['symbolBackground'] = self.config.get('Colors', 'symbolBackground')
            except ConfigParser.NoOptionError:
                pass

            try:
                self.colorConfig['separatorColor'] = self.config.get('Colors', 'separatorColor')
            except ConfigParser.NoOptionError:
                pass

            try:
                self.colorConfig['separatorBackground'] = self.config.get('Colors', 'separatorBackground')
            except ConfigParser.NoOptionError:
                pass


        self.ranges = [
            #{ 'name': 'ASCII', 
            # 'r' : range(33, 127)},
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

        self.colorDict = { 'black': '0'
                           , 'red': '1'
                           , 'green': '2'
                           , 'yellow': '3'
                           , 'blue': '4'
                           , 'magenta': '5'
                           , 'cyan': '6'
                           , 'white': '7'
                           , 'default': '9'
                           }


        self.cmdOptionsDict = {}
        self.cmdOptionsDict['help'] = { 'options' : ('h', 'help'),
                                        'arg' : None,
                                        'description' : 'help' }

        self.cmdOptionsDict['pager'] = { 'options' : ('p', 'pager'),
                                         'arg' : None,
                                         'description' : 'pager' }

        self.cmdOptionsDict['columns'] = { 'options' : ('c', 'columns'),
                                           'arg' : 'n',
                                           'description' : ('use <n> columns for output, '
                                                            'default is based on current terminal width') }

        self.cmdOptionsDict['output'] = { 'options' : ('o', 'output'),
                                           'arg' : 'outfile',
                                           'description' : 'output into <outfile>, default is stdout' }

        self.cmdOptionsDict['color'] = { 'options' : ('C', 'color'),
                                           'arg' : None,
                                           'description' : 'Use ANSI color output' }

        
        self.cmdOptionsDict['nocolor'] = { 'options' : ('N', 'nocolor'),
                                           'arg' : None,
                                           'description' : 'Disable ANSI color output' }


        self.cmdOptionsDict['sep'] = { 'options' : ('s', 'separator'),
                                       'arg' : 'sep',
                                       'description' : 'Use <sep> as column separator. Default is "|"' }
        


    def getCmdOptions(self):
        optList = []
        for e in self.cmdOptionsDict.itervalues():
            option = e['options'][0]
            if e['arg']:
                option = option + ':'
            optList.append(option)

        return ''.join(optList)


    def getCmdLongOptions(self):
        optList = []
        for e in self.cmdOptionsDict.itervalues():
            option = e['options'][1]
            if e['arg']:
                option = option + '='
            optList.append(option)

        return optList

    def genUsageString(self):
        bufList = []
        bufList.append(os.path.basename(sys.argv[0]))
        bufList.append('[OPTION]...')

        return ' '.join(bufList)
            
            
    def genHelp(self):
        optList = []
        bufList = []

        for e in self.cmdOptionsDict.itervalues():
            if e['arg']:
                option = '-%s <%s>, --%s=<%s>' % (e['options'][0],
                                               e['arg'],
                                               e['options'][1],
                                               e['arg'])
            else:
                option = '-%s, --%s' % e['options']

            optList.append((option, e['description']))

        maxlen = 0
        for option, description in optList:
            if len(option) > maxlen:
                maxlen = len(option)

        optList.sort()


        optTemplate = '%%-%ds' % maxlen
        lineTemplate = optTemplate + '  %s'

        for option, description in optList:
           bufList.append(lineTemplate % (option, description))

        bufList.append('\n')

        return '\n'.join(bufList)

            
    def getTerminalSize(self):
        rows, columns = os.popen('stty size', 'r').read().split()

        if int(rows) == 0:
            rows = 24
        if int(columns) == 0:
            columns = 80
        
        result = (int(rows), int(columns))
        
        return result

    def colorize(self, value, color, bgcolor):
        tempList = []
        
        tempList.append(chr(27))
        tempList.append('[3%sm' % self.colorDict[color])
        tempList.append(chr(27))
        tempList.append('[4%sm' % self.colorDict[bgcolor])
        tempList.append(value)
        tempList.append(chr(27))
        tempList.append('[0m')
        
        result = ''.join(tempList)
        return result
        
    def run(self, optlist, args):
        outfileName = None

        termRows, termCols = self.getTerminalSize()
        self.options['columns'] = termCols / 16

        #print self.options

        for o, i in optlist:
            if o in ('-h', '--help'):
                sys.stderr.write(self.genUsageString())
                sys.stderr.write('\n')
                sys.stderr.write(self.genHelp())
                sys.exit(1)

            elif o in ('-p', '--pager'):
                self.options['pager'] = True

            elif o in ('-c', '--columns'):
                try:
                    self.options['columns'] = int(i)
                except ValueError:
                    sys.stderr.write('Error: Invalid column value %s. Exiting...\n' % i)
                    sys.exit(1)

                if self.options['columns'] == 0:
                    sys.stderr.write('Error: Invalid column value 0. Exiting...\n')
                    sys.exit(1)

            elif o in ('-o', '--output'):
                outfileName = i

            elif o in ('-C', '--color'):
                self.options['color'] = True

            elif o in ('-N', '--nocolor'):
                self.options['color'] = False

            elif o in ('-s', '--separator'):
                self.options['sep'] = i
                

        if (self.options['pager'] and outfileName):
            sys.stderr.write('Warning: pager option overrides output option.\n')
            self.options['outfile'] = sys.stdout

        elif outfileName:
            outfile = open(outfileName, 'w')
            self.options['outfile'] = outfile
            
        codepointDict = self.codepoint2name()

        sep = self.options['sep']

        if self.options['outfile'] == sys.stdout:
            if self.options['color']:
                sep = self.colorize(self.options['sep'],
                                    self.colorConfig['separatorColor'],
                                    self.colorConfig['separatorBackground'])


        logList = []

        for rangeDict in self.ranges:
            count = 0;
            bufList = []
            r = rangeDict['r']

            logList.append('## %s' % rangeDict['name'])
            for i in r:
                if codepointDict.has_key(i):
                    codepoint = codepointDict[i]
                else:
                    codepoint = ' ' * 8

                if self.options['color']:
                    buf = self.columnTemplate % (i,
                                                 codepoint,
                                                 self.colorize(unichr(i),
                                                               self.colorConfig['symbolColor'],
                                                               self.colorConfig['symbolBackground']))
                    
                else:
                    buf = self.columnTemplate % (i,
                                                 codepoint,
                                                 unichr(i))

                bufList.append(buf)
                count = count + 1
                if (count % self.options['columns']) == 0:
                    logList.append(sep.join(bufList))
                    bufList = []
                    count = 0
            else:
                logList.append(sep.join(bufList))
                count = 0

        count = 0
        for line in logList:
                
            self.options['outfile'].write(line.encode('utf-8'))
            self.options['outfile'].write('\n')
            count = count + 1


            if self.options['pager']:
                if (count % (int(termRows)-2)) == 0:
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
    app = Henty()
    
    try:
        optlist, args = getopt.getopt(sys.argv[1:],
                                      app.getCmdOptions(),
                                      app.getCmdLongOptions())

    except getopt.error, msg:
        sys.stderr.write('ERROR: %s' % msg[0])
        sys.stderr.write('\n')
        sys.stderr.write(app.genUsageString())
        sys.stderr.write('\n')
        sys.stderr.write(app.genHelp())
        sys.stderr.write('\n')
        sys.exit(1)

    app.run(optlist, args)
    
    
    
    


