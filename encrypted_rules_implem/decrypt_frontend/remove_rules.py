import os
import re

for name in os.listdir("rules"):
    if int(re.findall("[0-9]+", name)[0]) > 1000:
        os.remove("rules/"+name)


