#!/usr/bin/env python

class s_1:
    def __init__(self):
        pass

    def setup(self):
        direction = {}
        print "Hello, World!"

        self.action(direction)

    def action(self, direction):
        response = ""
        while True:
            exit(0)
            response = get_response(self.__class__.__name__, direction)

    def cleanup(self):
        pass

pocket = {}
def get_response(caller, direction):
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
            exec caller + "_inst.cleanup()"
            exec "s_" + str(direction[response.split(" ")[1]])\
                + "_inst.setup()"
        else:
            print "\"" + response.split(" ")[1] + "\" is not a "\
                + "valid direction from this scene."
    else:
        return response

s_1_inst = s_1()
if __name__ == '__main__':
    s_1_inst.setup()