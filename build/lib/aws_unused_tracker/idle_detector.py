# idle_detector.py

from aws_unused_tracker.config import CPU_THRESHOLD_PERCENT, NETWORK_THRESHOLD_BYTES

def is_instance_idle(cpu_percent, network_mb):
    """
    Determines if an EC2 instance is idle based on CPU and network usage.
    Returns True if both CPU and network are below thresholds.
    """
    is_cpu_idle = cpu_percent < CPU_THRESHOLD_PERCENT
    is_network_idle = (network_mb * 1024 * 1024) < NETWORK_THRESHOLD_BYTES

    return is_cpu_idle and is_network_idle


def classify_instance(cpu_percent, network_mb):
    """
    Returns classification as 'Idle' or 'Active' with reason.
    """
    status = "Idle" if is_instance_idle(cpu_percent, network_mb) else "Active"

    reason = []
    if cpu_percent < CPU_THRESHOLD_PERCENT:
        reason.append("low CPU")
    else:
        reason.append("high CPU")

    if (network_mb * 1024 * 1024) < NETWORK_THRESHOLD_BYTES:
        reason.append("low network")
    else:
        reason.append("high network")

    return status, ", ".join(reason)

