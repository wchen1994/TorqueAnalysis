import COM
pt = COM.Point

x = pt(1,1,1)
y = pt(3,3,1)
result =  x + y
assert(result == pt(2,2,2))

points = COM.load_points("data.csv")
print points

com = pt(0,0,0)
for point in points:
    com += point
print com

print COM.compute_torque(com, 0)
