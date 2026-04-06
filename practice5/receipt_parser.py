# 1.
import re

txt = "abbb a ab aaaa"
pattern = r"ab*"

print(re.findall(pattern, txt))

# 2.
import re

txt = "ab abb abbb abbbb"
pattern = r"ab{2,3}"

print(re.findall(pattern, txt))

# 3.
import re

txt = "hello_world test_string notMatch Hello_World"
pattern = r"[a-z]+_[a-z]+"

print(re.findall(pattern, txt))

# 4.
import re

txt = "Hello World TEST Python Code"
pattern = r"[A-Z][a-z]+"

print(re.findall(pattern, txt))

# 5.
import re

txt = "a123b axxb a_b ac"
pattern = r"a.*b"

print(re.findall(pattern, txt))

# 6.
import re

txt = "Hello, world. Python is cool"
result = re.sub(r"[ ,\.]", ":", txt)

print(result)

# 7.
import re

def snake_to_camel(text):
    return re.sub(r"_([a-z])", lambda m: m.group(1).upper(), text)

print(snake_to_camel("hello_world_test"))

# 8.
import re

txt = "HelloWorldPython"
result = re.split(r"(?=[A-Z])", txt)

print(result)

# 9.
import re

txt = "HelloWorldPython"
result = re.sub(r"([A-Z])", r" \1", txt)

print(result.strip())

# 10.
import re

def camel_to_snake(text):
    return re.sub(r"([A-Z])", r"_\1", text).lower()

print(camel_to_snake("helloWorldTest"))