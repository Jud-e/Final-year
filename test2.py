compare = 5
var1 = 3
for i in range(10):
    if var1 > compare:
        compare = var1
    else:
        var1 = var1 + 1
        compare = compare
    print(compare)