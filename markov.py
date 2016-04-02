from smarkov import Markov


class MarkovNameGenerator():
    def __init__(self, infile, depth):
        fnames, lnames = self.load_names(infile)
        self.fname_model = Markov(fnames, depth)
        self.lname_model = Markov(lnames, depth)

    def make_names(self):
        while True:
            fname = ''.join(self.fname_model.generate_text())
            lname = ''.join(self.lname_model.generate_text())
            yield (fname + ' ' + lname).title()

    @staticmethod
    def load_names(infile):
        with open(infile) as f:
            names = [line.rstrip().split('\t') for line in f]
        return [name[0] for name in names], [name[1] for name in names]

