list1={1,2,3,'dog','cat',7,11,'bird'}
g='otter'
if g in list1 and type(g)==int: 
    print(f'Congrats! {g} is a number in the list!')
if g in list1 and type(g)==str: 
    print(f'Congrats! {g} is an animal in the list!')
else:
    print (f'Sorry, {g} is not in the list :(')