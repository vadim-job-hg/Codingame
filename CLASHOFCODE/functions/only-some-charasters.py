numbers = sum(c.isdigit() for c in s)
words   = sum(c.isalpha() for c in s)
spaces  = sum(c.isspace() for c in s)

s=''.join(i for i in s if i.isdigit())