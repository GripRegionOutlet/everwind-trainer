from __future__ import annotations

import argparse
import logging
import sys

from src.config.loader import load_config
from src.jobs.trainer_loop import TrainerLoop
from src.utils.logger import setup_logger


def cli_entry() -> int:
    parser = argparse.ArgumentParser(prog="everwind-trainer")
    parser.add_argument("--config", default="src/config/default.yaml")
    parser.add_argument("--dry-run", action="store_true",
                        help="validate pipeline without writing memory")
    parser.add_argument("--process", default="Everwind.exe",
                        help="target process name")
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args()

    setup_logger(args.log_level)
    log = logging.getLogger("everwind.trainer")

    cfg = load_config(args.config)
    log.info("Loaded config: %d features enabled", sum(1 for f in cfg.features.values() if f.enabled))

    loop = TrainerLoop(config=cfg, process_name=args.process, dry_run=args.dry_run)
    try:
        loop.run()
    except KeyboardInterrupt:
        log.info("Interrupt received, shutting down cleanly")
        loop.stop()
    return 0


if __name__ == "__main__":
    sys.exit(cli_entry())