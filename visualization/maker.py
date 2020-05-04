import networkx as nx
import networkx.algorithms.shortest_paths.generic as nxalgo
import matplotlib.pyplot as plt


def check_if_node_exists(graph, node):
    if graph.has_node(node) is False:
        graph.add_node(node, nodetype=node)


def check_if_edge_exists(graph, start, end):
    if graph.has_edge(start, end) is False:
        graph.add_edge(start, end)


class Maker:
    def __init__(self, activities_matrix, events_amount_matrix, alphas_matrix,
                 one_loops_matrix, two_loops_matrix, direct_dependency_matrix, long_distance_matrix, start_activities,
                 end_activities, dir_depend_threshold, one_loop_threshold, two_loops_threshold, long_dist_threshold,
                 relative_to_best, all_tasks_connected):
        self.activities_matrix = activities_matrix
        self.events_amount_matrix = events_amount_matrix
        self.alphas_matrix = alphas_matrix
        self.one_loops_matrix = one_loops_matrix
        self.two_loops_matrix = two_loops_matrix
        self.direct_dependency_matrix = direct_dependency_matrix
        self.long_distance_matrix = long_distance_matrix
        self.start_activities = start_activities
        self.end_activities = end_activities

        self.dir_depend_threshold = dir_depend_threshold
        self.one_loop_threshold = one_loop_threshold
        self.two_loops_threshold = two_loops_threshold
        self.long_dist_threshold = long_dist_threshold

        self.relative_to_best = relative_to_best
        self.all_tasks_connected = all_tasks_connected

    def print_all_matrix(self):
        print(self.activities_matrix)
        print(self.events_amount_matrix)
        print(self.alphas_matrix)
        print(self.one_loops_matrix)
        print(self.two_loops_matrix)
        print(self.direct_dependency_matrix)
        print(self.long_distance_matrix)
        print(self.start_activities)
        print(self.end_activities)

    def draw(self):
        graph = nx.MultiDiGraph()
        used_casualities = set()

        # draw alpha relations first
        self.draw_start(graph)
        self.draw_end(graph)
        self.draw_xor_relations(graph, used_casualities)
        self.draw_and_relations(graph, used_casualities)
        self.draw_casuality(graph, used_casualities)

        # draw heuristic relations
        self.draw_one_loops(graph)
        self.draw_two_loops(graph)
        self.draw_dir_dependency(graph)
        self.draw_long_distance(graph)

        labels = nx.get_node_attributes(graph, 'nodetype')
        colors = []
        for node,attr in graph.nodes(data=True):
            if attr.get('nodetype') == 'XOR':
                colors.append('lightcoral')
            elif attr.get('nodetype') == 'AND':
                colors.append('teal')
            elif attr.get('nodetype') == 'START' or attr.get('nodetype') == 'END':
                colors.append('sandybrown')
            else:
                colors.append('lightsteelblue')

        nx.draw_networkx(graph, labels = labels, node_color=colors, edge_color='Navy', node_size = 1000,
                         font_size = 14, font_weight = 'bold', edge_weight='bold', with_labels=True)
        plt.show()

    def draw_start(self, graph):
        graph.add_node('START', nodetype="START")
        if len(self.start_activities) == 1:
            graph.add_node(self.start_activities[0], nodetype=self.start_activities[0])
            graph.add_edge('START', self.start_activities[0])
        else:
            graph.add_node('startXOR', nodetype='XOR')
            graph.add_edge('start', 'startXOR')
            for i in range(0, len(self.start_activities)):
                graph.add_node(self.start_activities[i], nodetype=self.start_activities[i])
                graph.add_edge('startXOR', self.start_activities[i])

    def draw_end(self, graph):
        graph.add_node('END', nodetype='END')
        for i in range(0, len(self.end_activities)):
            check_if_node_exists(graph, self.end_activities[i])
            graph.add_edge(self.end_activities[i], 'END')

    def draw_xor_relations(self, graph, used_casualities):
        xor_table = []
        for i in range(0, len(self.alphas_matrix)):
            for j in range(0, len(self.alphas_matrix)):
                if i == j:
                    continue
                for k in range(0, len(self.alphas_matrix)):
                    if i == k or j == k:
                        continue
                    if (self.alphas_matrix[i][j] == 1 and self.alphas_matrix[i][k] == 1) and self.alphas_matrix[j][k] == 0:
                        check_if_node_exists(graph, self.activities_matrix[i])
                        check_if_node_exists(graph, self.activities_matrix[j])
                        check_if_node_exists(graph, self.activities_matrix[k])
                        xor_name = 'XOR '+self.activities_matrix[i]+'('+self.activities_matrix[j]+self.activities_matrix[k]+')'
                        xor_name_opposite = 'XOR '+self.activities_matrix[i]+'('+self.activities_matrix[k]+self.activities_matrix[j]+')'
                        if xor_name_opposite not in xor_table:
                            xor_table.append(xor_name)
                            graph.add_node(xor_name, nodetype='XOR')
                            graph.add_edge(self.activities_matrix[i], xor_name)
                            graph.add_edge(xor_name, self.activities_matrix[j])
                            graph.add_edge(xor_name, self.activities_matrix[k])
                            used_casualities.add(self.activities_matrix[i]+self.activities_matrix[j])
                            used_casualities.add(self.activities_matrix[i]+self.activities_matrix[k])

                    if (self.alphas_matrix[i][k] == 1 and self.alphas_matrix[j][k] == 1) and self.alphas_matrix[i][j] == 0:
                        check_if_node_exists(graph, self.activities_matrix[i])
                        check_if_node_exists(graph, self.activities_matrix[j])
                        check_if_node_exists(graph, self.activities_matrix[k])
                        xor_name = 'XOR '+'('+self.activities_matrix[i]+self.activities_matrix[j]+')'+self.activities_matrix[k]
                        xor_name_opposite = 'XOR '+'('+self.activities_matrix[j]+self.activities_matrix[i]+')'+self.activities_matrix[k]
                        if xor_name_opposite not in xor_table:
                            xor_table.append(xor_name)
                            #check_if_node_exists(graph, xor_name)
                            graph.add_node(xor_name, nodetype='XOR')
                            graph.add_edge(xor_name, self.activities_matrix[k])
                            graph.add_edge(self.activities_matrix[i], xor_name)
                            graph.add_edge(self.activities_matrix[j], xor_name)
                            used_casualities.add(self.activities_matrix[i] + self.activities_matrix[k])
                            used_casualities.add(self.activities_matrix[j] + self.activities_matrix[k])

    def draw_and_relations(self, graph, used_casualities):
        and_table = []
        for i in range(0, len(self.alphas_matrix)):
            for j in range(0, len(self.alphas_matrix)):
                if i == j:
                    continue
                for k in range(0, len(self.alphas_matrix)):
                    if i == k or j == k:
                        continue
                    if self.alphas_matrix[i][j] == 1 and self.alphas_matrix[i][k] == 1 and self.alphas_matrix[j][k] == 2:
                        check_if_node_exists(graph, self.activities_matrix[i])
                        check_if_node_exists(graph, self.activities_matrix[j])
                        check_if_node_exists(graph, self.activities_matrix[k])
                        and_name = 'AND '+self.activities_matrix[i]+'('+self.activities_matrix[j]+self.activities_matrix[k]+')'
                        and_name_opposite = 'AND '+self.activities_matrix[i]+'('+self.activities_matrix[k]+self.activities_matrix[j]+')'
                        if and_name_opposite not in and_table:
                            and_table.append(and_name)
                            #check_if_node_exists(graph, and_name)
                            graph.add_node(and_name, nodetype='AND')
                            graph.add_edge(self.activities_matrix[i], and_name)
                            graph.add_edge(and_name, self.activities_matrix[j])
                            graph.add_edge(and_name, self.activities_matrix[k])
                            used_casualities.add(self.activities_matrix[i] + self.activities_matrix[j])
                            used_casualities.add(self.activities_matrix[i] + self.activities_matrix[k])

                    if self.alphas_matrix[i][k] == 1 and self.alphas_matrix[j][k] == 1 and self.alphas_matrix[i][j] == 2:
                        check_if_node_exists(graph, self.activities_matrix[i])
                        check_if_node_exists(graph, self.activities_matrix[j])
                        check_if_node_exists(graph, self.activities_matrix[k])
                        and_name = 'AND '+'('+self.activities_matrix[i]+self.activities_matrix[j]+')'+ self.activities_matrix[k]
                        and_name_opposite = 'AND '+'('+self.activities_matrix[j]+self.activities_matrix[i]+')'+ self.activities_matrix[k]
                        if and_name_opposite not in and_table:
                            and_table.append(and_name)
                            #check_if_node_exists(graph, and_name)
                            graph.add_node(and_name, nodetype='AND')
                            graph.add_edge(and_name, self.activities_matrix[k])
                            graph.add_edge(self.activities_matrix[i], and_name)
                            graph.add_edge(self.activities_matrix[j], and_name)
                            used_casualities.add(self.activities_matrix[i] + self.activities_matrix[j])
                            used_casualities.add(self.activities_matrix[j] + self.activities_matrix[k])

    def draw_casuality(self, graph, used_casualities):
        for i in range(0, len(self.alphas_matrix)):
            for j in range(0, len(self.alphas_matrix[0])):
                if i == j:
                    continue
                if self.alphas_matrix[i][j] == 1:
                    if self.activities_matrix[i] + self.activities_matrix[j] not in used_casualities:
                        check_if_node_exists(graph, self.activities_matrix[i])
                        check_if_node_exists(graph, self.activities_matrix[j])
                        graph.add_edge(self.activities_matrix[i], self.activities_matrix[j])

    def draw_dir_dependency(self, graph):
        for i in range(0, len(self.direct_dependency_matrix)):
            for j in range(0, len(self.direct_dependency_matrix)):
                if i == j:
                    continue
                if self.direct_dependency_matrix[i][j] >= self.dir_depend_threshold:
                    check_if_edge_exists(graph, self.activities_matrix[i], self.activities_matrix[j])
                else:
                    if self.all_tasks_connected is False:
                        if graph.has_edge(self.activities_matrix[i], self.activities_matrix[j]):
                            graph.remove_edge(self.activities_matrix[i], self.activities_matrix[j])

    def draw_one_loops(self, graph):
        for i in range(0, len(self.one_loops_matrix)):
            if self.one_loops_matrix[i][i] >= self.one_loop_threshold > 0:
                check_if_node_exists(graph, self.activities_matrix[i])
                selfloop_name = 'selfloop'+self.activities_matrix[i]
                check_if_node_exists(graph, selfloop_name)
                graph.add_edge(self.activities_matrix[i], selfloop_name)
                graph.add_edge(selfloop_name, self.activities_matrix[i])

    def draw_two_loops(self, graph):
        for i in range(0, len(self.two_loops_matrix)):
            for j in range(0, len(self.two_loops_matrix)):
                if i == j:
                    continue
                if self.two_loops_matrix[i][j] >= self.two_loops_threshold:
                    if self.two_loops_matrix[j][i] >= self.two_loops_threshold:
                        check_if_node_exists(graph, self.activities_matrix[i])
                        check_if_node_exists(graph, self.activities_matrix[j])
                        check_if_edge_exists(graph, self.activities_matrix[i], self.activities_matrix[j])
                        check_if_edge_exists(graph, self.activities_matrix[j], self.activities_matrix[i])
                    else:
                        # if self.two_loops_matrix[i][j] >= self.dir_depend_threshold:
                        check_if_node_exists(graph, self.activities_matrix[i])
                        check_if_node_exists(graph, self.activities_matrix[j])
                        check_if_edge_exists(graph, self.activities_matrix[i], self.activities_matrix[j])
                        if self.all_tasks_connected is False:
                            if graph.has_edge(self.activities_matrix[j], self.activities_matrix[i]):
                                graph.remove_edge(self.activities_matrix[j], self.activities_matrix[i])
                else:
                    if self.two_loops_matrix[j][i] >= self.two_loops_threshold:
                        # if self.two_loops_matrix[j][i] >= self.dir_depend_threshold:
                        check_if_node_exists(graph, self.activities_matrix[j])
                        check_if_node_exists(graph, self.activities_matrix[i])
                        check_if_edge_exists(graph, self.activities_matrix[j], self.activities_matrix[i])
                        if self.all_tasks_connected is False:
                            if graph.has_edge(self.activities_matrix[i], self.activities_matrix[j]):
                                graph.remove_edge(self.activities_matrix[i], self.activities_matrix[j])
                    else:
                        if self.all_tasks_connected is False:
                            if graph.has_edge(self.activities_matrix[i], self.activities_matrix[j]):
                                graph.remove_edge(self.activities_matrix[i], self.activities_matrix[j])
                        if self.all_tasks_connected is False:
                            if graph.has_edge(self.activities_matrix[j], self.activities_matrix[i]):
                                graph.remove_edge(self.activities_matrix[j], self.activities_matrix[i])

    def draw_long_distance(self, graph):
        for i in range(0, len(self.long_distance_matrix)):
            for j in range(0, len(self.long_distance_matrix)):
                if i == j:
                    continue
                if self.long_distance_matrix[i][j] >= self.long_dist_threshold:
                    check_if_node_exists(graph, self.activities_matrix[i])
                    check_if_node_exists(graph, self.activities_matrix[j])
                    check_if_edge_exists(graph, self.activities_matrix[i], self.activities_matrix[j])
               # else:
                    # if self.all_tasks_connected is False:
               #     if graph.has_edge(self.activities_matrix[i], self.activities_matrix[j]):
               #         graph.remove_edge(self.activities_matrix[i], self.activities_matrix[j])
