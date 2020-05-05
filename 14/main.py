#!/usr/bin/env python3

import argparse
import icu
import os
import re
import socket
import sys
import time
import concurrent.futures

host = '52.49.91.111'
port = '2092'

master_running = True
master_id = 9
sybil_ids = []

# parse list of servers from line
def extract_server_list(line_str):
    regex_servers = 'servers: \\[[0-9]+(,[0-9]+)*\\]'
    m = re.search(regex_servers, line_str)
    if m is None:
        print('why is this none? -->', line_str)
    assert m is not None
    return [int(x) for x in line_str[m.start():m.end()][10:-1].split(',')]

# parse secret owner from line
def extract_secret_owner(line_str):
    regex_owner = 'secret_owner: [0-9]+'
    m = re.search(regex_owner, line_str)
    if m is None: return None
    return int(line_str[m.start():m.end()][14:])

def extract_own_id(line_str):
    regex_serverid = 'SERVER ID: [0-9]+'
    m = re.search(regex_serverid, line_str)
    if m is None: return None
    return int(line_str[m.start():m.end()][11:])

def extract_msg_sender(line_str):
    regex_sender = ': [0-9]+ ->'
    m = re.search(regex_sender, line_str)
    if m is None: sender = None
    else: sender = int(line_str[m.start():m.end()][2:-3])
    return sender

def extract_prepare_id(line_str):
    regex_id = 'PREPARE {[0-9]+,[0-9]+}'
    m = re.search(regex_id, line_str)
    assert m is not None
    return line_str[m.start():m.end()][8:]

def prepare_msg(seq_number, my_id):
    return 'PREPARE {%d,%d}' % (seq_number, my_id)

def accept_msg(seq_number, my_id, next_servers, next_owner):
    return 'ACCEPT {id: {%d,%d}, value: {servers: %s, secret_owner: %d}}' % \
           (seq_number, my_id, str(next_servers).replace(' ', ''), next_owner)

def promise_msg(proposal_id, prev_proposal):
    return 'PROMISE %s %s' % (proposal_id, prev_proposal)

def broadcast_message(sock, id, msg, servers):
    print('broadcasting %s to %s' % (msg, servers))
    for server in servers:
        if server is not id:
            sock.send(('%s -> %d\n' % (msg, server)).encode('ascii'))

def send_message(sock, id, msg, receiver):
    broadcast_message(sock, id, msg, [receiver])

def get_node_to_remove(servers, owner, master, sybils):
    removables = set(servers)
    removables = removables.difference(set(sybils))
    removables = removables.difference([owner, master])
    if len(removables) == 0: return None
    return removables.pop()

def get_node_to_add(servers, owner, master, sybils):
    missing_sybils = set(sybils).difference(servers)
    if len(missing_sybils) == 0: return None
    return missing_sybils.pop()

def get_next_membership(servers, owner, master, sybils):
    # check if we have sybils of ours missing
    node_to_add = get_node_to_add(servers, owner, master, sybils)
    if node_to_add is not None:
        print('Decision - Membership Change - Add', node_to_add)
        return list(set(servers).union([node_to_add]))

    # check if we can shoot down other nodes
    node_to_remove = get_node_to_remove(servers, owner, master, sybils)
    if node_to_remove is not None:
        print('Decision - Membership Change - Remove' ,node_to_remove)
        return list(set(servers).difference([node_to_remove]))

    return None

def we_have_majority(servers, sybils):
    return 2 * (len(sybils) + 1) > len(servers)

def run_sybil_node(id, sock):
    global sybil_ids
    sybil_ids.append(id)
    sock.settimeout(1)
    while master_running:
        try:
            data = sock.recv(1048576)
            if not data: break
        except socket.timeout: continue
    sock.close()

def run_master_node(id, sock):
    global master_running
    proposal_id = 10
    promises = []
    step = 0
    while master_running:
        data = sock.recv(1048576)
        if not data:
            break
        lines = data.decode('ascii').splitlines()
        for line in lines:
            #print('[%2d] %s' % (id, line))

            # broadcast the proposal everyone has ever seen
            if step == 0 and 'ROUND FINISHED' in line:
                promises = []
                servers = extract_server_list(line)
                owner = extract_secret_owner(line)
                msg = prepare_msg(proposal_id, id)
                broadcast_message(sock, id, msg, servers)
                step = 1

            # collect promises -- if we have enough, do something nasty
            if step == 1 and 'PROMISE' in line:
                #print(line)
                promises.append(extract_msg_sender(line))
                #print('got promises:', promises, 'from servers:', servers)
                # check if we have promises from majority of acceptors
                if 2 * len(promises) > len(servers):
                    # check if we are already a majority of the member nodes
                    if we_have_majority(servers, sybil_ids):
                        msg = accept_msg(proposal_id, id, servers, id)
                        broadcast_message(sock, id, msg, servers)
                    # we are not the majority (yet) - lets move closer to that goal
                    else:
                        membership = get_next_membership(servers, owner, id, sybil_ids)
                        assert membership is not None
                        msg = accept_msg(proposal_id, id, membership, owner)
                        broadcast_message(sock, id, msg, servers)
                    proposal_id += 10
                    step = 0

            if 'SECRET IS' in line:
                print(line)
                step = 0
                master_running = False
                break
    master_running = False
    sock.close()

def spawn_node():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, int(port)))
    data = sock.recv(15)
    lines = data.decode('ascii').splitlines()
    id = extract_own_id(data.decode('ascii').splitlines()[0])
    assert id is not None
    if id == master_id: run_master_node(id, sock)
    else:               run_sybil_node(id, sock)

num_nodes = 4
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for i in range(0, num_nodes):
        futures.append(executor.submit(spawn_node))
    for future in concurrent.futures.as_completed(futures):
        future.result()

