with open("dragonsChromatic.html","r") as f:
    lines = f.read()


line_split_list = lines.split("<h2></h2>")
#print(line_split_list[0])
print(len(line_split_list))
index = 0
for els in line_split_list:
    with open("chromDrag%s.html"%index,"w") as f:
        f.write(els)
        index+=1