#!/usr/bin/env python

class s_1:
    def __init__(self):
        self.__namespace = {}

    def setup(self):
        direction = {}
        self.__namespace['n'] = 0
        while [tests]:
            print "Okay."
            self.__namespace['n'] = self.__namespace['n'] + 1
        return self.action(direction)

    def action(self, direction):
        response = ""
        while True:
            exit(0)
            response = get_response(direction)
            if isinstance(response, list):
                self.cleanup()
                return response[0]

    def cleanup(self):
        pass



pocket = {}
def get_response(direction):
    response = raw_input(" -->> ")
    response = response.lower()
    response = response.translate(None,
                "!#$%&'()*+,-./:;<=>?@[\]^_`{|}~")
    response = ' '.join(response.split())
    if response == "exit":
        print "== GAME TERMINATED =="
        exit(0)
    elif response[:5] == "move " and len(response.split(" ")) == 2:
        if response.split(" ")[1] in direction:
            return ["s_" + str(direction[response.split(" ")[1]])\
                + "_inst.setup()"]
        else:
            print "\"" + response.split(" ")[1] + "\" is not a "\
                + "valid direction from this scene."
    else:
        return response

s_1_inst = s_1()
if __name__ == '__main__':
    next = s_1_inst.setup()
    while True:
        exec 'next = ' + next