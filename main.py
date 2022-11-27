a = '/First/Second/Third/Fourth/Fifth'
b="/".join(a.strip("/").split('/')[0:])

print(b)