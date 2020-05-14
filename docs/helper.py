import random

class Parser:

    def __init__(self,filename):
        self.currentSub = ''
        self.prevSection = ''
        self.prevSubSection = ''
        self.prevSubSubSection = ''
        self.section = ''
        self.sections = {}
        self.types = {}
        self.names = {}
        self.order = []
        self.blanklines = 0
        self.filename = filename

    def savePrevSection(self):
        if self.prevSection == self.currentSub:
            self.sections[self.prevSection] = self.section
            self.types[self.prevSection] = 'section'
            self.names[self.prevSection] = self.prevSection
            self.order.append(self.prevSection)
        elif self.prevSubSection == self.currentSub:
            self.sections[self.prevSection + '>' + self.prevSubSection] = self.section
            self.types[self.prevSection + '>' + self.prevSubSection] = 'subsection'
            self.names[self.prevSection + '>' + self.prevSubSection] = self.prevSubSection
            self.order.append(self.prevSection + '>' + self.prevSubSection)
        elif self.prevSubSubSection == self.currentSub:
            self.sections[self.prevSection + '>' + self.prevSubSection + '>' + self.prevSubSubSection] = self.section
            self.types[self.prevSection + '>' + self.prevSubSection + '>' + self.prevSubSubSection] = 'subsubsection'
            self.names[self.prevSection + '>' + self.prevSubSection + '>' + self.prevSubSubSection] = self.prevSubSubSection
            self.order.append(self.prevSection + '>' + self.prevSubSection + '>' + self.prevSubSubSection)

    def parseInput(self):
        content = []
        with open (self.filename, 'rt') as f:
            content = f.read().split('\n')

        for l in content:
            if '\\section{' in l:
                self.savePrevSection()
                self.section = ''

                self.prevSection = l[9:-1]
                self.currentSub = l[9:-1]
            elif '\\subsection{' in l:
                self.savePrevSection()
                self.section = ''

                self.prevSubSection = l[12:-1]
                self.currentSub = l[12:-1]
            elif '\\subsubsection{' in l:
                self.savePrevSection()
                self.section = ''

                self.prevSubSubSection = l[15:-1]
                self.currentSub = l[15:-1]
            else:
                if l != '':
                    self.section = self.section + l + '\n'
                    self.blanklines = 0
                elif self.blanklines < 3:
                    self.section = self.section + l + '\n'
                    self.blanklines = self.blanklines + 1
                else:
                    self.blanklines = self.blanklines + 1
        self.savePrevSection()


    def rebuildOutput(self):
        with open(self.filename, "w") as f:
            for s in self.order:
                if s == '':
                    f.write(self.sections[s])
                else:
                    f.write('\\'+self.types[s]+'{'+self.names[s]+'}\n')
                    f.write(self.sections[s])


chapters = {}
chapters['background']=Parser('Chapters_Research/1background.tex')
chapters['method']=Parser('Chapters_Research/2method.tex')
chapters['software']=Parser('Chapters_Research/3software.tex')
#chapters.['results']=Parser('Chapters_Research/4results.tex')
#chapters['evaluation']=Parser('Chapters_Research/5evaluation.tex')


for p in chapters.values():
    p.parseInput()

run = True
while run:
    random_chapter_key = random.choice(list(chapters.keys()))
    random_chapter = chapters[random_chapter_key]
    random_key = random.choice(random_chapter.order)
    with open("EDITME.tex", "w") as f:
        f.write(random_chapter.sections[random_key])
    print('Work on\n==',random_key,'==\nsection from the',random_chapter_key, 'chapter now.')
    print('Edit and save EDITME.tex and input an option:')
    print('0 : build output and exit')
    print('1 : next section')
    i = input()
    #print('hi',i,'bye')
    if i == 0 or i == '0':
        run = False
    with open("EDITME.tex", "r") as f:
        random_chapter.sections[random_key] = f.read()
    for p in chapters.values():
        p.rebuildOutput()

for p in chapters.values():
    p.rebuildOutput()

