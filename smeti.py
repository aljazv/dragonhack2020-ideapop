def find_closest(data, x, y, amount_x, amount_y, amount_z):
    final_array = []
    
    curr_x = x + amount_x
    curr_y = y + amount_y
    curr_z = data[curr_x][curr_y] 
    print(curr_x, curr_y, curr_z)
    while True:
        if curr_x > len(data) or curr_y > len(data[0]):
            return None
        calculated_z = data[curr_x][curr_y]
        if abs(calculated_z - curr_z) < 1:
            return (curr_x, curr_y)
        else:
            curr_x += amount_x
            curr_y += amount_y
            curr_z += amount_z     
        
find_closest(test, x=0,y=0, amount_x=110, amount_y=20, amount_z=100)

def closest_oglisce(T, shape):
    # T = (x,y)
    # za točko T najde najbližjo točko z znanim podatkom o višini
    T_new = (round(T[0]), round(T[1]))
    if T_new[0] == shape[0]:
        T_new = (T_new[0]-1, T_new[1])
    if T_new[0] == -1:
        T_new = (0, T_new[1])
    if T_new[1] == shape[1]:
        T_new = (T_new[0], T_new[1]-1)
    if T_new[1] == -1:
        T_new = (T_new[0], 0)
    return (int(T_new[0]), int(T_new[1]))

def build_ray_arree(data, x, y, amount_x, amount_y):
    final_array = []
    data = np.array(list(map(list, zip(*data))))
    ray_trace = []
    print(data[:2,:5])
    curr_x = x 
    curr_y = y
    while not (curr_x > len(data) or curr_y > len(data[0]) or curr_x < 0 or curr_y < 0):
        print(round(curr_x,2), round(curr_y,2))

        ray_trace.append((curr_x, curr_y))
        cl_x, cl_y = closest_oglisce((curr_x, curr_y), data.shape)
        final_array.append((data[cl_x][cl_y], (curr_x,curr_y)))
        curr_x += amount_x
        curr_y += amount_y
    
    print(ray_trace)
    return final_array, ray_trace

#print(test)
#r = build_ray_arree(test, x=0,y=0, amount_x=0.7, amount_y=0.1);
#print(r)

z = np.array([100,70,30,20,60,80,90,100,120,40,20,145,170])
