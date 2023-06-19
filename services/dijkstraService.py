from math import inf

class DijkstraService:
    def __init__(self) -> None:
        pass
    
    def findAll(self, wmat, start, end=-1):
        """
        Returns a tuple with a distances' list and paths' list of
        all remaining vertices with the same indexing.

            (distances, paths)

        For example, distances[x] are the shortest distances from x
        vertex which shortest path is paths[x]. x is an element of
        {0, 1, ..., n-1} where n is the number of vertices

        Args:
        wmat    --  weighted graph's adjacency matrix
        start   --  paths' first vertex
        end     --  (optional) path's end vertex. Return just the 
                distance and its path

        Exceptions:
        Index out of range, Be careful with start and end vertices
        """
        n = len(wmat)

        dist = [inf]*n
        dist[start] = wmat[start][start]  # 0

        spVertex = [False]*n
        parent = [-1]*n

        path = [{}]*n

        for count in range(n-1):
            minix = inf
            u = 0

            for v in range(len(spVertex)):
                if spVertex[v] == False and dist[v] <= minix:
                    minix = dist[v]
                    u = v

            spVertex[u] = True
            for v in range(n):
                if not(spVertex[v]) and wmat[u][v] != 0 and dist[u] + wmat[u][v] < dist[v]:
                    parent[v] = u
                    dist[v] = dist[u] + wmat[u][v]

        for i in range(n):
            j = i
            s = []
            while parent[j] != -1:
                s.append(j)
                j = parent[j]
            s.append(start)
            path[i] = s[::-1]

        return (dist[end], path[end]) if end >= 0 else (dist, path)


    def findShortestPath(self, wmat, start, end=-1):
        return self.findAll(self, wmat, start, end)[1]


    def findShortestDistance(self, wmat, start, end=-1):
        """
        Returns distances' list of all remaining vertices.

        Args:
        wmat    --  weigthted graph's adjacency matrix
        start   --  paths' first vertex
        end     --  (optional) path's end vertex. Return just
                the distance

        Exceptions:
        Index out of range, Be careful with start and end vertices.
        """
        return self.findAll(self, wmat, start, end)[0]