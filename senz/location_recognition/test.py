# -*- encoding=utf-8 -*-
__author__ = 'daiyue'

import json
import location

file = open("testLocation.json")
jsonArray = json.load(file)["results"]
file.close()

print(location.cluster(jsonArray))