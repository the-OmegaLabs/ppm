def printMultiLines(text):
    for i in text.split("\\n"):
        if i:
            print(f"{i}")