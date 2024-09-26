import os
from datetime import datetime

def log_register(objeto, message):
    log_folder = f"log/{objeto}"

    env_var = f"{objeto.upper()}_LOG"
    log_enabled = os.getenv(env_var, 'N')
    all_log_enabled = os.getenv('ALL_LOG', 'N')

    if log_enabled != 'Y' and all_log_enabled != 'Y':
        print(f"Logging for '{objeto}' is disabled.")
        return

    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    current_date = datetime.now().strftime("%Y%m%d")
    log_file = os.path.join(log_folder, f"{objeto}_{current_date}.log")

    with open(log_file, 'a') as f:
        log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{log_time}] {message}\n")

    print(f"Log saved in: {log_file}")