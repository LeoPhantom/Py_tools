import pefile
import json

exports_list = []

pe =pefile.PE("C:\\Windows\\System32\\kernel32.dll")
for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
    try:
        exports_list.append(exp.name.decode("UTF-8"))
    except:
        continue

exports_json = {"exports": exports_list}
open("exports.json", "wb").write(json.dumps(exports_json).encode())
