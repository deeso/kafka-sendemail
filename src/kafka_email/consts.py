KAFKA_EMAIL = 'kafka-email'
SMTP_HOST = 'smtp_host'
SMTP_PORT = 'smtp_port'
SMTP_USERNAME = 'smtp_username'
SMTP_PASSWORD = 'smtp_password'
SMTP_USE_TLS = 'smtp_use_tls'
SMTP_LEVEL = 'smtp_level'

EMAIL_CONFIG = 'email_config'
CONSUMER_CONFIG = 'consumer_config'
PRODUCER_CONFIG = 'producer_config'

DEFAULT_SMTP_HOST = '127.0.0.1'
DEFAULT_SMTP_PORT = 25
DEFAULT_SMTP_USERNAME = None
DEFAULT_SMTP_PASSWORD = None
DEFAULT_SMTP_USE_TLS = True
DEFAULT_SMTP_LEVEL = 0

DEFAULT_EMAIL_CONFIG = {
    SMTP_HOST: DEFAULT_SMTP_HOST,
    SMTP_PORT: DEFAULT_SMTP_PORT,
    SMTP_USERNAME: DEFAULT_SMTP_USERNAME,
    SMTP_PASSWORD: DEFAULT_SMTP_PASSWORD,
    SMTP_USE_TLS: DEFAULT_SMTP_USE_TLS,
}


FILENAME = 'filename'
BUFFERED_CONTENT = 'buffered_content'
CONTENT = 'content'
CONTENT_TYPE = 'content_type'
CC = 'cc'
BCC = 'bcc'

KAFKA_COMPONENT = 'kafka_component'
PRODUCER = 'producer'
CONSUMER = 'consumer'
KAFKA_BROKER = 'kafka_broker'
KAFKA_TOPIC = 'kafka_topic'
KAFKA_GROUP = 'kafka_group'
KAFKA_CLIENT_ID = 'kafka_client_id'
KAFKA_PATTERN = 'kafka_pattern'

BROKER = 'broker'
TOPIC_SEND_EMAIL = 'send_emails'
DEFAULT_CONSUMER_GROUP = 'send_emais_consumer'
EARLIEST = 'earliest'

KAFKA_TIMEOUT = 'kafka_timeout'
KAFKA_SLEEP = 'kafka_sleep'
KAFKA_PERFORM_MP = 'kafka_perform_mp'

DEFAULT_KAFKA_TIMEOUT = 2
DEFAULT_KAFKA_SLEEP = 5
DEFAULT_BROKER="127.0.0.1:9092"
DEFAULT_KAFKA_CLIENT_ID = None
DEFAULT_KAFKA_PERFORM_MP = False
DEFAULT_KAFKA_CONFIG = {
    KAFKA_BROKER: DEFAULT_BROKER,
    KAFKA_TOPIC: TOPIC_SEND_EMAIL,
    KAFKA_GROUP: DEFAULT_CONSUMER_GROUP,
    KAFKA_CLIENT_ID: None,
    KAFKA_PATTERN: None,
    KAFKA_SLEEP: DEFAULT_KAFKA_SLEEP,
    KAFKA_TIMEOUT: DEFAULT_KAFKA_TIMEOUT,
    KAFKA_PERFORM_MP: DEFAULT_KAFKA_PERFORM_MP
    # KAFKA_COMPONENT: None,
}

NUM_PROCESSES = 'num_processes'
DEFAULT_NUM_PROCESSES = 4
SUBJECT = 'subject'
BODY = 'body'
FILENAMES_CONTENTS = 'filenames_contents'