# from here  http://codegists.com/snippet/python/teads-sponsored-contestpy_workofartiz_python
from collections import defaultdict

edges = defaultdict(list)
for i in range(int(input())):
    xi, yi = [int(j) for j in input().split()]
    edges[xi].append(yi)
    edges[yi].append(xi)


# calculates the maximum depth (not going back)
def max_depth(came_from, node):
    # if leaf node
    if len(edges[node]) == 1:
        return 0

    depth = 0

    for child in edges[node]:
        if came_from == child:
            continue
        depth = max(depth, 1 + max_depth(node, child))

    return depth


# pick just any node to be the root of the tree
root = xi

# get max_depths of all children of the root
depths = (1 + max_depth(root, child) for child in edges[root])

# sort the depths to easily get the top 1 or 2
depths = sorted(depths, reverse=True)

# calculate the cost of the longest path
max_chain = depths[0] + depths[1] if len(depths) > 1 else depths[0]

# print max cost
print("%d" % (max_chain / 2 + max_chain % 2))