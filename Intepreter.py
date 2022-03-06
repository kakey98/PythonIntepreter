from typing import *
INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(type = self.type, value = self.value)

    def __rpre__(self):
        return self.__str__()

    
class Intepreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token: Union[Token, None] = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        text = self.text

        if self.pos > len(self.text) - 1:
            return Token(EOF, None)

        current_char = text[self.pos]

        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token

        
        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        if current_char == '-':
            token = Token(MINUS, current_char)
            self.pos += 1
            return token
        
        self.error

    
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        self.current_token = self.get_next_token()

        left = Token(INTEGER,0)
        while (self.current_token.type == INTEGER):
            left = Token(INTEGER, left.value * 10 + self.current_token.value)
            self.eat(INTEGER)


        op = self.current_token
        if op.type == PLUS:
            self.eat(PLUS)
        elif op.type == MINUS:
            self.eat(MINUS)
        else:
            self.error()

        right = Token(INTEGER,0)
        while (self.current_token.type == INTEGER):
            right = Token(INTEGER, right.value * 10 + self.current_token.value)
            self.eat(INTEGER)

        if op.type == PLUS:
            result = left.value + right.value
        elif op.type == MINUS:
            result = left.value - right.value
        else:
            raise Exception("Type of operator is invalid")


        return result
        

def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break

        if not text:
            continue
        intepreter = Intepreter(text)
        result = intepreter.expr()
        print(result)

if __name__ == "__main__":
    main()