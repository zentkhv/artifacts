import logging
import colorlog


class Logger:
    def __init__(self):
        self.logger = logging.getLogger('custom_logger')
        self.logger.setLevel(logging.DEBUG)  # Установим уровень на DEBUG, чтобы видеть все уровни логов

        # Создание консольного обработчика
        console_handler = logging.StreamHandler()

        # Создание формата логов с использованием colorlog
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s[%(asctime)s] - %(message)s',
            datefmt='%H:%M:%S %d/%m/%Y',
            log_colors={
                'DEBUG': 'blue',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )

        # Установка формата для обработчика
        console_handler.setFormatter(formatter)

        # Добавление обработчика к логгеру
        self.logger.addHandler(console_handler)

    def log(self, message, level='info'):
        match level:
            case 'debug':
                self.logger.debug(message)
            case 'info':
                self.logger.info(message)
            case 'warning':
                self.logger.warning(message)
            case 'error':
                self.logger.error(message)
            case 'critical':
                self.logger.critical(message)
            case _:
                self.logger.info(message)


logger = Logger()

if __name__ == "__main__":
    logger.log('Это сообщение с текущей датой и временем.')
    logger.log('Это сообщение уровня DEBUG.', level='debug')
    logger.log('Это предупреждение.', level='warning')
    logger.log('Это сообщение об ошибке.', level='error')
    logger.log('Это критическое сообщение.', level='critical')
