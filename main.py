import re
from math import isclose 

class Answer:
    def __init__(self, representation):
        self.repr = representation
        try:
            values = [str(eval(representation))]
        except:
            values = re.findall('-?\d*\.?\d*', representation)
        self.values = list(filter(None, values))
    
    def __len__(self):
        return len(self.values)
    
    def __str__(self):
        return self.repr
    
    def __repr__(self):
        return self.repr
        
        
        
class Parser:
    def __init__(self, string, coma_pb = False):
        self.string = string
        if coma_pb:
            self.string = string.replace(',', '.')
        
        Lines = self.string.split("\n")
        self.equation = self._get_equation(Lines[0])
        self.Answers = self._get_answers(Lines[1:])
        
        self.parse()
        
    def __repr__(self):
        return ''
    
    def _get_equation(self, line):
        line = line.replace('÷', '/')
        temp = line.split('=')
        return temp[0] + ' - (' + temp[1] + ' )'
        
    def _get_answers(self, List):
        Answers = [self._parse_proposition(prop) for prop in List]
        return list(filter(None, Answers))
        
    def _parse_proposition(self, proposition):
        return Answer(proposition)
    
    def _test_valid_answers(self):
        it = iter(self.Answers)
        the_len = len(next(it))
        if not all(len(l) == the_len for l in it):
            raise ValueError('not all answers have the same size!')
    
    def _test_answer(self, answer):
        local_equation = self.equation
        if self.number_variables == 1:
            value = eval(local_equation.replace('?', answer.values[0]))
        else:
            for variable in answer.values:
                local_equation = local_equation.replace('?', variable, 1)
            value = eval(local_equation)
        if isclose(0, value, abs_tol=1e-4):
            return True
        else:
            return False

    def parse(self):
        print('Equation: {}'.format(self.equation))
        print('Propositions: {}'.format(self.Answers))        
        self._test_valid_answers()
        
        self.number_variables = len(self.Answers[0])
        for answer in self.Answers:
            if self._test_answer(answer):
                print('It worked, the correct answer is {}'.format(answer))

                
if __name__ == '__main__':
    Parser("""(42 ÷ ?) ÷ (3 + ?) = 2

3 et -24
3 et 4
4 et 3
-72 et 3 """)
    Parser("""5 / ? = ? / 20

 
5
 
12
 
10
 
15
""")
    Parser("""( 21 / 44  -  2 / 8)  ÷  ?  =  1	
4 / 22
5 / 22
3 / 8
4 / 8
6 / 8 """)
