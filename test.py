a = [1, 2, 3, 4]
s = ['a', 'b', 'c', 'd']

b = list(zip(a, s))

l = [1, 3, 2, 4]

for i in range(len(l)):
	for j in range(len(l)):
		if i == j and a[i] != l[i]:
			l1 = i
			l2 = l.index(a[i])
			a[l1], a[l2] = a[l2], a[l1]
			s[l1], s[l2] = s[l2], s[1]

print(a)
print(s)