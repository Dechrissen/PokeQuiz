with open('./branch.txt', 'r') as f:
    lines = f.readlines()
new_lines = []
for line in lines:
    line = line.strip('\n')
    new_lines.append(line)

str_list = str(new_lines)
with open('./branches.txt', 'w') as f:
    f.write(str_list)
