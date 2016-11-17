import os
import re

for name in os.listdir("rules"):
    if int(re.findall("[0-9]+", name)[0]) > 100:
        os.remove("rules/"+name)


