import cPickle
import gzip
import re
import argparse
from operator import itemgetter

class NamaeWa(object):
    dict_array = None
    longest_word = 10

    def build_map(self, sourcefile):
        self.dict_array = cPickle.load(sourcefile)

    def extract_name(self, source_string):
        base_string = source_string.split('@')[0]
        base_string = re.sub('[0-9]{1,}', ' ', base_string)

        guessed_names = []

        #special cases
        #contains (.) break into words and finish
        if ('.' in base_string):
            guessed_names = self.axe_twoletter_names(base_string.split('.'))
        elif ('_' in base_string):
            guessed_names = self.axe_twoletter_names(base_string.split('_'))
        elif ('-' in base_string):
            guessed_names = self.axe_twoletter_names(base_string.split('-'))
        else:
            guessed_names = [self.break_string(base_string)]

        if len(guessed_names) <= 0:
            guessed_names = [base_string]

        return guessed_names[0].capitalize()

    def axe_twoletter_names(self, name_array):
        return [name for name in name_array if len(name) > 2]

    def break_string(self, source_string):
        wc = 0
        str_length = len(source_string)
        max_length = self.longest_word
        words = {}

        if (str_length < self.longest_word):
            max_length = str_length

        for n in range(str_length):
            words[wc] = ((source_string[n: n+1]), 0)
            m = 1
            test = words.get(wc, '')

            found = False
            while m <= max_length and (n + m) < str_length:
                test = (test[0] + source_string[n+m:n+m+1], test[1])

                if test[0].lower() in self.dict_array:
                    words[wc] = (test[0], int(self.dict_array[test[0].lower()]))
                    k = m
                    found = True

                m += 1

            if found:
                n = k + 1
            else:
                n += 1
            wc += 1


        components = []
        for key, value in words.iteritems():
            if value[1] > 0 and len(value[0]) > 2:
                components.append(value)

        # components = sorted(components, key=itemgetter(1), reverse=True)

        if len(components) <= 0:
            return source_string

        return components[0][0]



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('email')
    args = parser.parse_args()
    with gzip.open('static/names.pklzip', 'rb') as o_file:
        extractor = NamaeWa()
        extractor.build_map(o_file)

    print "First name (best guess): " + extractor.extract_name(args.email)
