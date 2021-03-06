"""
Damon Jones

The Gale Effect
0.0.1.1
"""

import json
import sys

class parser:
    def __init__(self):
        self.tokens = []

    def add_token(self, type, value = ""):
        if value != "":
            type += ":" + value
        self.tokens.append(type)

    def parse(self):
        data = ""
        with open("The Gale Effect/Data/Test Story.story", "r") as f:
            data = f.read()

        token_type = ""
        token_data = ""
        token_finished = False
        new_line_scheduled = False

        for char in data:
            if token_type == "":
                if char == '"':
                    token_type = "string"
                elif char == "[":
                    token_type = "array"
                elif char in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r",
                              "s", "t", "u", "v", "w", "x", "y", "z"]:
                    token_type = "id"
                elif char == "$":
                    token_type = "macro"

            if char == "\n":
                new_line_scheduled = True

            if token_type == "id":
                if char in [' ', '\n']:
                    token_finished = True
                else:
                    token_data += char
            if token_type == "string":
                if char == '"' and len(token_data) > 0:
                    token_finished = True
                token_data += char
            if token_type == "array":
                if char == "]":
                    token_finished = True
                token_data += char
            if token_type == "macro":
                if char in [' ', '\n']:
                    token_finished = True
                elif char != "$":
                    token_data += char

            if token_finished:
                self.add_token(token_type, token_data)
                token_type = ""
                token_data = ""
                token_finished = False
            if new_line_scheduled:
                self.add_token("endline")
                new_line_scheduled = False
        print(self.tokens)


def prompt(input_prompt: str, keywords: list, invalid_message: str = "Invalid Input",
           case_specific: bool = False) -> str:
    while True:
        print("\n")
        loc_user_in = input(input_prompt)
        if not case_specific:
            loc_user_in = loc_user_in.lower()
        for keyword in keywords:
            if keyword in loc_user_in:
                return keyword
        else:
            print(invalid_message)


def load_file(file_dir: str) -> dict:
    return json.load("Saves/" + file_dir)


def save_file(file_name: str, save_data: dict):
    with open("Saves/" + file_name + ".json", "w+") as f:
        json.dump(save_data, f)

print("=======================")
print("\n    The Gale Effect")
print("=======================")
input("Press enter to start...")


# Load Files Prompt
user_in = prompt("Load from save? [y/n] ", ["y", "n"])
if user_in == "y":
    pass

with open("The Gale Effect/Data/Test Story.story", "r") as f:
    x = parser()
    x.parse()
    story = x.tokens

game_finished = False
current_statement = ""
current_args = []

scope = []
scope_args = []

macros = {}

for i in range(len(story) - 1):
    token = story[i]
    scope_index = len(scope) - 1

    value = ""
    split_token = token.split(":", 1)
    type = split_token[0]
    if len(split_token) > 1:
        value = split_token[1]

    if type == "id":
        if current_statement == "":
            current_statement = value
        else:
            current_args.append(value)
    elif type == "macro":
        if value in macros:
            current_args.append(macros[value])
    elif type == "string":
        current_args.append(value.replace("\"", ""))
    elif type == "array":
        current_args.append(eval(value))

    # end-line finalizes the statement purpose
    elif type == "endline":
        is_execute = True
        if len(scope) > 0:
            if not scope_args[scope_index]:
                is_execute = False

        if is_execute:
            if current_statement == "set":
                macros[current_args[0]] = current_args[1]
            elif current_statement == "text":
                print(current_args[0])
            elif current_statement == "texts":
                for item in current_args:
                    print(item)
            elif current_statement == "prompt":
                user_in = prompt(current_args[0], current_args[1])
            elif current_statement == "exit":
                sys.exit(1)
        if current_statement == "switch":
            scope.append("s")
            scope_args.append("switch")
        if current_statement == "case":
            scope.append("c")
            if current_args[0] == user_in:
                scope_args.append(True)
            else:
                scope_args.append(False)
        elif current_statement == "end":
            scope_args.pop()
            scope.pop(scope_index)

        current_statement = ""
        current_args = []