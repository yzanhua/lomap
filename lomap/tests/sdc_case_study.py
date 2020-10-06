#! /usr/bin/python

# Test case for using Weighted Finite State Error Systems for task substitution
# Copyright (C) 2020, Cristian-Ioan Vasile (cvasile@lehigh.edu)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from __future__ import print_function

import networkx as nx

from lomap import Fsa, Ts, Wfse, ts_times_wfse_times_fsa
from lomap.algorithms import product
import matplotlib.pyplot as plt
import numpy as np


def fsa_constructor():

    # Define the set ofatomic propositions
    ap = set(['T1', 'T2', 'T3', 'T4','T5', 'O'])


    # Avoid the obstacle region until visiting T1
    specs = ['!O U T1'] # task deletion and substitution case
    # specs = ['F T1'] #canonical case
 

    fsa = Fsa(props=ap, multi=False) # empty FSA with propsitions from `ap`
    for spec in specs:
        fsa.from_formula(spec)

    ## Visualize the automata

    # nx.draw(fsa.g, with_labels=True)
    # plt.show()

    return fsa


def ts_constructor():

    ts = Ts(directed=True, multi=False)
    ts.g = nx.DiGraph()
    ts.g.add_nodes_from([0,1,2,3,4,5,6,7,8,9,10,12])

    ts.g.add_weighted_edges_from([(0,12,1), (12,4,0),(12,7,4),(12,6,6),(7,3,0),(7,8,3),(8,2,0),(12,10,1),(10,5,0),(10,6,3),(6,9,2),(9,1,0)])

    ts.init[(0)] = 1

    ## Add lables to TS nodes

    ts.g.add_node((1), attr_dict={'prop': set(['T1'])})  
    ts.g.add_node((2), attr_dict={'prop': set(['T2'])})
    ts.g.add_node((3), attr_dict={'prop': set(['T3'])})
    ts.g.add_node((4), attr_dict={'prop': set(['T4'])})
    ts.g.add_node((5), attr_dict={'prop': set(['T5'])})
    ts.g.add_node((6), attr_dict={'prop': set(['O'])})

    ## Visualize the TS
    # nx.draw(ts.g , with_labels=True, node_color='b')
    # plt.show()

    return ts


def wfse_constructor():
    ap = set(['T1', 'T2', 'T3', 'T4','T5','O']) # set of atomic propositions
    wfse = Wfse(props=ap, multi=False)
    wfse.init = set() # HACK

    # add states
    wfse.g.add_nodes_from(['q0', 'q1', 'q2', 'q3','q4'])

    # add transitions
    pass_through_symbols = [(symbol, symbol, 1) for symbol in wfse.prop_bitmaps
                            if symbol >= 0]
    # print('pass through symbols:', pass_through_symbols)
    wfse.g.add_edge('q0', 'q0', attr_dict={'symbols': pass_through_symbols})

    print("Please enter your preference: 1 - Deletion, 2 - Substitution")
    user_preference = raw_input()
    print(user_preference)

    if (user_preference == '1'): 

        print("deletion")

        in_symbol = wfse.bitmap_of_props(set(['T2']))
        out_symbol = wfse.bitmap_of_props(set())

        weighted_symbols = [(in_symbol, out_symbol, 2)]

        # Substitute T3 by T1 with a penalty 4
        in_symbol = wfse.bitmap_of_props(set(['T3']))
        out_symbol = wfse.bitmap_of_props(set())
        weighted_symbols = [(in_symbol, out_symbol, 4)]
        wfse.g.add_edge('q0', 'q2', attr_dict={'symbols': weighted_symbols})
        weighted_symbols = [(-1, out_symbol, 4)]    
        wfse.g.add_edge('q2', 'q0', attr_dict={'symbols': weighted_symbols})

        # Substitute T4 by T1 with a penalty 6
        in_symbol = wfse.bitmap_of_props(set(['T4']))
        out_symbol = wfse.bitmap_of_props(set())
        weighted_symbols = [(in_symbol, out_symbol, 6)]
        wfse.g.add_edge('q0', 'q3', attr_dict={'symbols': weighted_symbols})
        weighted_symbols = [(-1, out_symbol, 6)]
        wfse.g.add_edge('q3', 'q0', attr_dict={'symbols': weighted_symbols})


        # Substitute T5 by T1 with a penalty 8
        in_symbol = wfse.bitmap_of_props(set(['T5']))
        out_symbol = wfse.bitmap_of_props(set())
        weighted_symbols = [(in_symbol, out_symbol, 8)]
        wfse.g.add_edge('q0', 'q4', attr_dict={'symbols': weighted_symbols})
        weighted_symbols = [(-1, out_symbol, 8)]
        wfse.g.add_edge('q4', 'q0', attr_dict={'symbols': weighted_symbols})

    elif (user_preference == '2'): 
        print("substitution")

        # Substitute T2 by T1 with a penalty 2
        in_symbol = wfse.bitmap_of_props(set(['T2']))
        out_symbol = wfse.bitmap_of_props(set(['T1']))

        weighted_symbols = [(in_symbol, out_symbol, 2)]
        wfse.g.add_edge('q0', 'q1', attr_dict={'symbols': weighted_symbols})

        weighted_symbols = [( -1, out_symbol, 2)] 
        wfse.g.add_edge('q1', 'q0', attr_dict={'symbols': weighted_symbols})

        # Substitute T3 by T1 with a penalty 4
        in_symbol = wfse.bitmap_of_props(set(['T3']))
        out_symbol = wfse.bitmap_of_props(set(['T1']))
        weighted_symbols = [(in_symbol, out_symbol, 4)]
        wfse.g.add_edge('q0', 'q2', attr_dict={'symbols': weighted_symbols})
        weighted_symbols = [(-1, out_symbol, 4)]    
        wfse.g.add_edge('q2', 'q0', attr_dict={'symbols': weighted_symbols})

        # Substitute T4 by T1 with a penalty 6
        in_symbol = wfse.bitmap_of_props(set(['T4']))
        out_symbol = wfse.bitmap_of_props(set(['T1']))
        weighted_symbols = [(in_symbol, out_symbol, 6)]
        wfse.g.add_edge('q0', 'q3', attr_dict={'symbols': weighted_symbols})
        weighted_symbols = [(-1, out_symbol, 6)]
        wfse.g.add_edge('q3', 'q0', attr_dict={'symbols': weighted_symbols})


        # Substitute T5 by T1 with a penalty 8
        in_symbol = wfse.bitmap_of_props(set(['T5']))
        out_symbol = wfse.bitmap_of_props(set(['T1']))
        weighted_symbols = [(in_symbol, out_symbol, 8)]
        wfse.g.add_edge('q0', 'q4', attr_dict={'symbols': weighted_symbols})
        weighted_symbols = [(-1, out_symbol, 8)]
        wfse.g.add_edge('q4', 'q0', attr_dict={'symbols': weighted_symbols})

    else : 

        print("invalid choice")

    # set the initial state
    wfse.init.add('q0')

    # set the final state
    wfse.final.add('q0')

    # nx.draw(wfse.g, with_labels=True)
    # nx.draw_networkx_edge_labels(wfse.g,pos=nx.spring_layout(wfse.g))
    # plt.show()

    return wfse


def main():
    fsa = fsa_constructor()
    print(fsa)
    ts = ts_constructor()
    print(ts)
    wfse = wfse_constructor()
    print(wfse)

    product_model = ts_times_wfse_times_fsa(ts, wfse, fsa)

    print('Product: Init:', product_model.init) # initial states
    print('Product: Final:', product_model.final) # final states

    # get initial state in product model -- should be only one
    # Convert the sets of initial and final states into lists
    init_states = list(product_model.init)
    final_states = list(product_model.final)
    dijkstra_length = []    # This list stores the Dijkstra path lengths for all final states 


    # Iterate over all final states and find the correponding path lenths and paths
    for each_state in product_model.final: 

        length = nx.dijkstra_path_length(product_model.g, init_states[0], each_state,weight='weight')
        dijkstra_length.append(length)

    if (not dijkstra_length):
        print("Task execution is not possible")
        return


    # Get the index corresponding to the minimum cost and retrieve the corresponding final state

    pa_optimal_index = np.argmin(dijkstra_length)
    pa_optimal_final_state = final_states[pa_optimal_index]
    print("pa_optimal_final_state:", pa_optimal_final_state)

    # Find out the min length path with the optimal final state as a target using Dijkstra 
    pa_optimal_path = nx.dijkstra_path(product_model.g, init_states[0],pa_optimal_final_state,weight='weight')

    # Obtain the individual optimal paths for each component 
    ts_optimal_path, wfse_state_path, fsa_state_path = zip(*pa_optimal_path)

    print('TS: Optimal Trajectory:', ts_optimal_path)
    print('WFSE: Optimal Trajectory:', wfse_state_path)
    print('FSA: Optimal Trajectory:', fsa_state_path)

    print('Symbol translations:')
    for ts_state, state, next_state in zip(ts_optimal_path[1:], pa_optimal_path,
                                           pa_optimal_path[1:]):
        transition_data = product_model.g[state][next_state]
        original_symbol, transformed_symbol = transition_data['prop']
        print(ts_state, ':', original_symbol, '->', transformed_symbol)


if __name__ == '__main__':
    main()
