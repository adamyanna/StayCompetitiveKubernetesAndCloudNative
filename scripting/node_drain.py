#! /usr/bin/venv python3

import os
import sys
import time
import datetime
from symbol import argument

# import cloud sdk from CSP

# Drain all running pods from node (except daemonset pods)
KUBE_NODE_DRAIN_CMD = "kubectl drain %s --ignore-daemonsets --delete-emptydir-data"
# Uncordoning node to let scheduler use node
KUBE_NODE_UNCORDON_CMD = "kubectl uncordon %s"

def log(msg, level="info"):
    if level not in ("info", "debug", "warning", "error"):
        print("error: log level invalid!")
    print("[%s][%f]: %s\n" % (level, datetime.datetime.now().timestamp(), msg))

def run_command(command):
    try:
        result = os.system(command)
        if result != 0:
            # Do error handing
            log("os.system running error %s" % result, "error")
        return result
    except Exception as e:
        # Do error logging & handing
        log("os.system running exception %s" % e, "error")


def kube_drain_node(node_name):
    """
    Cordoning the node & evict all running pods (except daemonset)
    :param node_name: string
    :return:
    """
    log("Cordoning the node & evict all running pods (except daemonset) %s" % node_name, "info")
    # call kubectl
    drain_result = run_command(KUBE_NODE_DRAIN_CMD % node_name)
    # handing output
    print(drain_result)


def kube_uncordon_node(node_name):
    log("uncordoning the node %s" % node_name, "info")
    uncordon_result = run_command(KUBE_NODE_UNCORDON_CMD % node_name)
    # handing output
    print(uncordon_result)

def kube_validating_node(node_name):
    log("validating node %s" % node_name, "info")
    run_command("kubectl get node %s" % node_name)


def kube_work_node_maintenance():
    # call cloud sdk to reboot os for woker node or terminate or do some diagnose
    pass

if __name__ == '__main__':
    arguments = sys.argv[1:]
    node_name = arguments[0]

    kube_drain_node(node_name)
    kube_uncordon_node(node_name)