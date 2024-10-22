# samson.py

# This is a simple stochastic chatbot. 
#
# Its main memory is a dictionary matching positions in the memory
# to corresponding "tokens", where a "token" consists of any string
# of consecutive non-whitespace characters. Strings of whitespace 
# characters are skipped over and treated as single spaces.
#
# There is also a special end-message token (ASCII RS).
#
# We also maintain an index, mapping tokens to a list of positions where
# that token exists in the memory.
#
# The main loop is basically just:
#   - 1. Obtain an input message from the user; 
#           break it into tokens; append them to the memory.
#   - 2. Repeat the following until end-message is encountered:
#       a. Retrieve the locations of the most recent token 
#           from the memory index.
#       b. Pick one of those locations at random.
#       c. Append the next token to the output.

import random

END_MSG_TOKEN = '\x1e'  # ASCII record separator (RS) control character.

# Function to tokenize a message string.
def tokenize(msg):
    """Break a message into tokens."""
    # Split the message into words and punctuation.
    tokens = []
    while len(msg) > 0:
        # Skip over whitespace before the start of a token
        while len(msg) > 0 and msg[0].isspace():
            msg = msg[1:]

        # Find the next sequence of non-whitespace characters.
        token = ''
        while len(msg) > 0 and not msg[0].isspace():
            token += msg[0]
            msg = msg[1:]
        if len(token) > 0:
            #print(f"Identified token: {token}")  # Diagnostic print statement
            tokens.append(token)
    return tokens

class Memory:
    def __init__(self):
        self._tokens = {}   # Map from position to token.
        self._index = {}    # Map from token to list of positions.
        self.add_token(END_MSG_TOKEN)
            # This starts the memory off with a message boundary.

    @property
    def _nToks(self):
        return len(self._tokens)
    
    def add_token(self, token):
        """Add a token to the memory."""
        pos = self._nToks
        self._tokens[pos] = token
        if token not in self._index:
            self._index[token] = []
        self._index[token].append(pos)

    def add_message(self, msg):
        """Add a message to the memory."""
        tokens = tokenize(msg)
        for token in tokens:
            self.add_token(token)
        self.add_token(END_MSG_TOKEN)
    
    def get_token(self, pos):
        """Return the token at a position."""
        return self._tokens[pos]
    
    def get_last_token(self):
        """Return the last token in the memory."""
        last_position = self._nToks - 1
        return self._tokens[last_position]
    
    def get_positions(self, token):
        """Return the positions of a token in the memory."""
        return self._index.get(token, [])
    
# Main loop
def main():

    memory = Memory()

    # Greet the user.
    first_message = "Hello! I am Samson. I am a simple chatbot. :)"
    memory.add_message(first_message)

    print()
    print("Samson:\t " + first_message)
    print()

    while True:
        msg = input("User:\t ")
        memory.add_message(msg)
        print()

        print("Samson:\t", end="")

        token = memory.get_last_token()
        while True:
            positions = memory.get_positions(token)
            if len(positions) == 0: # This should never happen.
                break

            # Select a random position from the list of positions,
            # except we never select the last position in the memory.
            while True:
                pos = random.choice(positions)
                if pos != memory._nToks - 1:
                    break

            # Advance to the next position in the memory.
            pos += 1
            
            # Retrieve that next token.
            token = memory.get_token(pos)

            # If the token is the end-message token, then we're done.
            if token == END_MSG_TOKEN:
                break
            
            # Output a space character, followed by the token.
            print(f" {token}", end="")

        print('\n')     # End the line of output and add a blank line.

if __name__ == "__main__":
    main()
