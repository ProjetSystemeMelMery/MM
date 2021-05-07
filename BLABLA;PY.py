
import logging

print = logging.info
logging.basicConfig(level=logging.WARNING if args.quiet else logging.INFO,
                    format="%(message)s")