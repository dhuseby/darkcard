class Reader(object):

    @staticmethod
    def read(f, delim='----', joiner='\n'):
        l = []
        with open(f, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip('\r\n')
                if line == delim:
                    return joiner.join(l)
                l.append(line)

