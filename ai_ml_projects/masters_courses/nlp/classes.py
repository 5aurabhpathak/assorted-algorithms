#Object oriented aspect of code. Contains classes used by other modules
from nltk.corpus import names

class NounPhrase:

    def __init__(self, np):
        self.np = np
        self.gender = None
        self.name = " ".join(np.leaves())
        self.person = 'third'
        self.number = None
        self.__calculateAgreement()

    def __calculateAgreement(self):
        if len(self.np) == 1:
            if self.np[0,0] in names.words('male.txt'): self.gender = 'male'
            elif self.np[0,0] in names.words('female.txt'): self.gender = 'female'

        if {'NNS', 'NNPS'}.intersection({b for (a, b) in self.np.pos()}) or {',','and'}.intersection(self.np.leaves()):
            self.number = {'plural'}
        else:
            self.number = {'singular'}
        if 'PRP' in self.np[0].label():
            if self.np[0,0].lower() in {'they', 'them', 'themselves', 'their'}: self.number = {'plural'}
            elif self.np[0,0].lower() in {'him', 'he', 'himself'}:
                self.gender = 'male'
                self.number = {'singular'}
            elif self.np[0,0].lower() in {'her', 'herself' , 'she'}:
                self.number = {'singular'}
                self.gender = 'female'
            elif self.np[0,0].lower() in {'it', 'itself'}: self.number = {'singular'}
            elif self.np[0,0].lower() in {'us', 'we', 'our', 'ourselves'}:
                self.number = {'plural'}
                self.person = 'first'
            elif self.np[0,0].lower() in {'I', 'me', 'my', 'myself'}:
                self.number = {'singular'}
                self.person = 'first'
            elif self.np[0,0].lower() in {'yourself'}:
                self.number = {'singular'}
                self.person = 'second'
            elif self.np[0,0].lower() in {'you', 'your'}:
                self.number = {'singular', 'plural'}
                self.person = 'second'
            elif self.np[0,0].lower() in {'yourselves'}:
                self.number = {'plural'}
                self.person = 'second'

    def agreeswith(self, e):
        if e.np[0].label() in {'PRP', 'PRP$'}: return False
        if not self.number.intersection(e.number): return False
        if self.gender != e.gender: return False
        if self.person != e.person: return False
        return True

class Entity(NounPhrase):
    def __init__(self, np, parsetree, sentencenum):
        super().__init__(np)
        self._parsetree = parsetree
        self.salience = self._calculateSalience()
        self.sentencenum = sentencenum
        self.phrases = {self.name}

    def _calculateSalience(self):
        sal = 100
        if self.np is self._parsetree[0,0]: sal += 80
        if self.np.parent().label() == 'VP':
            if self.np.parent()[0,0].lower() in {'exists', 'is', 'be', 'was', 'were', 'occur', 'appear', 'appeared', 'existed', 'occured', 'happen', 'happened'}: sal += 120
            if len(self.np.parent()) > 2 and self.np.parent()[2].label() == 'NP' and self.np.parent()[2] is not self.np: sal += 40
            else: sal += 50
        if self.np.parent().label() == 'PP' and self.np.parent().parent().label() != 'VP': sal += 50
        if self.np.parent().label() == 'NP' and self.np is self.np.parent()[0]: sal += 80
        elif self._headnoun():
            sal+= 80
        return sal

    def _headnoun(self):
        np = self.np
        while np.parent():
            if np.parent().label() == 'NP': return False
            np = np.parent()
        return True

    def __str__(self):
        return 'name: ' + self.name + '\n\t' + str(self.np) + '\n\tgender: ' + str(self.gender) + '\n\tnumber: ' + str(self.number) + '\n\tperson: ' + self.person + '\n\tphrases: ' + str(self.phrases) + '\n\tsalience: ' + str(self.salience) + '\n\tin sentence: ' + str(self.sentencenum)

def ispleonastic(np, pt):
    if pt[0,0] is not np: return False
    sent = pt.leaves()
    modaladj = {'advised', 'obvious', 'paramount', 'certain', 'enough'
                'necessary', 'unnecessary', 'good', 'nice', 'possible', 'probable', 'obligatory', 'required', 'determined', 'likely', 'time', 'uncertain'}
    modalverb = {'might', 'may', 'can', 'could', 'shall', 'should', ',ust'}
    pp = {'to', 'for', 'that'}
    if sent[1] in {'is', 'was', 'were'} and sent[2] in modaladj and sent[3] in pp: return True
    elif sent[1] in modalverb and 'that' in sent[2:]: return True
    elif sent[1] in {'seems', 'appears', 'follows'} and {'that', 'to'}.intersection(sent[2:]): return True
    return False
