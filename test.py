participants = ["A", "B", "C"]

stack = [
    "B.func1->ret2", [
        "loop myloop", [
            "alt ok", [
                "B._test$func3", [
                    ".func5", [
                        ".func2", [
                            "C.CREATE",
                            ".func4"
                        ]
                    ],
                    ".func6"
                ]
            ],
            "else test1", [".ok"],
            "else test2", [".nok"],
            "C.func"
        ]
    ]
]



c = participants[0]

def display(current, node, level):
    i = 0
    indent = " " * (level *3)
    while(i < len(node)):
        x = node[i]
        if isinstance(x, str):
            if (x[:3] == "alt") or (x[:3] == "opt"):
                print(f"{indent}{x}")
                display(current, node[i+1], level+1)
                i += 1
                while  i+1 < len(node) and isinstance(node[i+1], str) and node[i+1][:4] == "else":
                    i += 1
                    print(f"{indent}{node[i]}")
                    display(current, node[i+1], level+1)
                    i += 1
                print(f"{indent}end")

                
            elif x[:4] == "loop":
                print(f"{indent}{x}")
                display(current, node[i+1], level+1)
                print(f"{indent}end")
                i += 1
            elif x[0] == ".":
                
                isblock =  (i+1 < len(node)) and isinstance(node[i+1], list)
                elem = x[1:].replace("$", ".")
                if isblock:
                    print(f"{indent}{current} -> {current}: {elem}")
                    print(f"{indent}activate {current}")
                    display(current, node[i+1], level+1)
                    print(f"{indent}deactivate {current}")
                    i += 1
                else:
                    print(f"{indent}{current} ->> {current}: {elem}")
                    
            elif (x.find(".") != -1):

                pos = x.find(".")
                ret = "ret"
                if x.find("->") != -1:
                    pos2 = x.find("->")
                    elem = x[pos+1:pos2]
                    ret = x[pos2+2:]
                else: 
                    elem = x[pos+1:]
                elem = elem.replace("$", ".")
                new = x[:pos]
                print(f"{indent}{current} ->>+ {new}: {elem}")
                if (i+1 < len(node)) and isinstance(node[i+1], list):
                    display(new, node[i+1], level+1)
                    i += 1
                print(f"{indent}{new} ->>- {current}: {ret}")
            else:
                print(f"{indent}{current} -> {current}: {x}")
        i += 1

print("""
```mermaid
sequenceDiagram
""")

for p in participants:
    print(f"participant {p}")
       
display(participants[0], stack, 0)

print("```")
                
