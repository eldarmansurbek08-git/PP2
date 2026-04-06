# 1
# import re
# txt = input()
# s = re.match("Hello",txt)
# if s:
#     print("Yes")
# else:
#     print("No")

# 2
# import re
# txt = input()
# txt2 = input()
# s = re.search(txt2,txt)
# if s:
#     print("Yes")
# else:
#     print("No")

# 3
# import re 
# txt = input()
# txt2 = input()
# s = re.findall(txt2,txt)
# print(len(s))

# 4
# import re
# txt = input()
# digits = re.findall(r"\d",txt)
# print(" ".join(digits))

# 5
# import re
# txt = input()
# s = re.match(r"^[A-Za-z].*[0-9]$",txt)
# if s:
#     print("Yes")
# else:
#     print("No")

# 6
# import re
# txt = input()
# p = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]+"
# m = re.search(p, txt)
# if m:
#     print(m.group())
# else:
#     print("No email")

# 7
# import re
# txt1 = input()
# txt2 = input()
# txt3 = input()
# s = re.sub(txt2,txt3,txt1)
# print(s)

# 8
# txt = input()
# words = txt.split()
# cnt = 0
# if len(words) == 3:
#     cnt += 1
# print(cnt)