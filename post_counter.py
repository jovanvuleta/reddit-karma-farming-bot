bot_name_here = ""
f = open(f"posts_replied_to-{bot_name_here}.txt", 'r')
lines = f.read().split(',')
print(len(lines))
