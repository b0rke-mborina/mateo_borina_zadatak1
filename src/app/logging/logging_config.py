import logging

def setup_logging(log_file: str = "src/app/logging/app.log", level: int = logging.INFO) -> None:
	formatter = logging.Formatter(
		"%(asctime)s [%(levelname)s] %(name)s: %(message)s"
	)

	# file handler
	file_handler = logging.FileHandler(log_file)
	file_handler.setLevel(level)
	file_handler.setFormatter(formatter)

	# console handler
	console_handler = logging.StreamHandler()
	console_handler.setLevel(level)
	console_handler.setFormatter(formatter)

	# root logger
	root_logger = logging.getLogger()
	root_logger.setLevel(level)

	# avoid adding handlers multiple times
	if not root_logger.handlers:
		root_logger.addHandler(file_handler)
		root_logger.addHandler(console_handler)
