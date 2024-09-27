import sys
from app import create_app
from flask_twisted import Twisted
from twisted.python import log

if __name__ == "__main__":
    app = create_app()
    twisted = Twisted(app)
    log.startLogging(sys.stdout)

    app.logger.info("Running the app...")

    # Twisted 서버 실행
    twisted.run(port=5000)  # 원하는 포트로 변경 가능