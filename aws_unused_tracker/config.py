# config.py

# ----------- CloudWatch Settings -----------
# Time range (in days) to pull metrics
METRIC_LOOKBACK_DAYS = 7

# Metric polling interval (in seconds)
METRIC_PERIOD = 3600 * 6  # 6 hours

# ----------- EC2 Thresholds -----------
CPU_THRESHOLD_PERCENT = 5.0       # below this % = idle
NETWORK_THRESHOLD_BYTES = 10 * 1024 * 1024  # 10 MB = idle

# ----------- EBS Thresholds (to be used later) -----------
EBS_READ_THRESHOLD = 10
EBS_WRITE_THRESHOLD = 10

# ----------- ELB Thresholds (to be used later) -----------
ELB_REQUEST_THRESHOLD = 100

# ----------- Output Settings -----------
EXPORT_JSON = True
EXPORT_CSV = True
EXPORT_DIR = "output"

# ----------- Logging -----------
ENABLE_LOGGING = True
LOG_FILE = "tracker.log"

