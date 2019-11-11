# python3 mains/run_ulm.py -config internal/dev-test-persist-mongo-service-config.toml
from kafka_email.service import EmailSenderService
from kafka_email.config import Config
import time
import argparse
import sys


CMD_DESC = 'start the Kafka Email Service.'
parser = argparse.ArgumentParser(description=CMD_DESC)
parser.add_argument('-config', type=str, default=None,
                    help='config file containing client information')


args = parser.parse_args()

if args.config is None:
    print ('config file is required')
    sys.exit(1)

Config.parse_config(args.config)

eml_service = EmailSenderService.from_config()
print (eml_service.__dict__)
eml_service.run()

try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    pass

EmailSenderService.stop()
sys.exit(0)