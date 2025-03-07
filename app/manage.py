#!/usr/bin/env python
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    from app.management.setup_commands import cli, setup_commands
    setup_commands()
    cli()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
