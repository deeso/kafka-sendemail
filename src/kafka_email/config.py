from .consts import *
import toml


class Config(object):
    CONFIG = {}

    @classmethod
    def check_raise(cls, block_name, key, value):
        if value is None:
            raise Exception("'%s':'%s' requires a value"%(block_name, key))

    @classmethod
    def parse_config(cls, config_file):
        try:
            with open(config_file) as f:
                toml_str = f.read()
            toml_data = toml.loads(toml_str)
            cls.parse_kafka_block(toml_data)

        except:
            raise

    @classmethod
    def parse_kafka_block(cls, toml_data):
        block = toml_data.get(KAFKA_EMAIL)

        for k, v in block.items():
            cls.CONFIG[k] = v

        ct = block.get(KAFKA_COMPONENT, 'producer')
        cls.CONFIG[KAFKA_COMPONENT] = ct

        email_config = {}
        for k, v in DEFAULT_EMAIL_CONFIG.items():
            v = block.get(k, v)
            email_config[k] = v

        cls.CONFIG[EMAIL_CONFIG] = email_config

        consumer_config = {}
        for k, v in DEFAULT_KAFKA_CONFIG.items():
            v = block.get(k, v)
            consumer_config[k] = v

        cls.CONFIG[CONSUMER_CONFIG] = consumer_config

    @classmethod
    def check_at_least_one(cls, name):
        return len(cls.CONFIG.get(name, {})) > 0


    @classmethod
    def get(cls):
        return cls.CONFIG

    @classmethod
    def set_value(cls, key, value):
        cls.CONFIG[key] = value

    @classmethod
    def get_value(cls, key):
        return cls.CONFIG.get(key, None)



