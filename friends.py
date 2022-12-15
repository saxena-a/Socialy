class Graph:
    def __init__(self,graph_dict):
        self.graph_dict = graph_dict

    def get_paths(self,start,end,path=[]):
        path = path + [start]
        if start==end:
            return [path]

        if start not in self.graph_dict:
            return []
        paths = []
        for node in self.graph_dict[start]:
            if node not in path:
                new_paths =self.get_paths(node,end,path)
                for p in new_paths:
                    paths.append(p)
        return paths

    def get_shortest_path(self,start,end,path=[]):
        path = path + [start]

        if start not in self.graph_dict:
            return None

        if start==end:
            return path

        shortest_path = None
        for node in self.graph_dict[start]:
            if node not in path:
                sp = self.get_shortest_path(node,end,path)
                if sp:
                    if shortest_path is None or len(sp)<len(shortest_path):
                        shortest_path = sp
        return shortest_path


def getFriends(users,user):
    friends_graph = Graph(users)
    friendsConnections = {
        0: [],
        1: [],
        2: [],

    }
    for friend in users:
        if(user==friend):
            continue

        if (friends_graph.get_shortest_path(user, friend) == None):

            friendsConnections[0].append(friend)
            continue

        if(len(friends_graph.get_shortest_path(user,friend))==2):

            friendsConnections[1].append(friend)

        if len(friends_graph.get_shortest_path(user,friend))>2:
            friendsConnections[2].append(friend)

    return friendsConnections
