import os
import argparse
from subprocess import check_call
import socket
import random

def detect_port(port):
    '''Detect if the port is used, return True if the port is used'''
    socket_test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        socket_test.connect(('127.0.0.1', int(port)))
        socket_test.close()
        return True
    except:
        return False

def find_port():
    '''Find a port which is free'''
    port = random.randint(5000, 10000)
    while detect_port(port):
        port = random.randint(5000, 10000)
    return port

def start_container(image, name):
    '''Start docker container'''
    port = find_port()
    cmds = ['docker', 'run', '-d', '-p', str(port) + ':22', '--name', name, image]
    check_call(cmds)
    print(port)

def stop_container(name):
    '''Stop docker container'''
    stop_cmds = ['docker', 'container', 'stop', name]
    check_call(stop_cmds)
    rm_cmds = ['docker', 'container', 'rm', name]
    check_call(rm_cmds)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', required=True, choices=['start', 'stop'], dest='mode', help='start or stop a container')
    parser.add_argument('--name', required=True, dest='name', help='the name of container to be used')
    parser.add_argument('--image', dest='image', help='the image to be used')
    args = parser.parse_args()
    if args.mode == 'start':
        start_container(args.image, args.name)
    else:
        stop_container(args.name)
