import json
import time
import urllib.error as urllib_error
from ansible.module_utils.urls import socket

try:
    from ..common.hv_api_constants import API
    from ..common.hv_log import Log
    from ..common.vsp_constants import Endpoints
    from .ansible_url import open_url
except ImportError:
    from common.hv_api_constants import API
    from common.hv_log import Log
    from common.vsp_constants import Endpoints
    from .ansible_url import open_url

logger = Log()


class SingletonClass(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SingletonClass, cls).__new__(cls)
        return cls.instance


class SessionManager(SingletonClass):
    current_sessions = {}
    retry_count = 0

    def get_current_session(self, connection_info):
        logger.writeDebug("generate_token current_sessions = {}", self.current_sessions)
        key = self.current_sessions.get(connection_info.address, None)
        if key is not None:
            return self.current_sessions.get(connection_info.address)
        else:
            token = self.generate_token(connection_info)
            self.current_sessions[connection_info.address] = token
            return token

    def renew_session(self, connection_info):
        unused = self.current_sessions.pop(connection_info.address, None)
        token = self.generate_token(connection_info)
        self.current_sessions[connection_info.address] = token
        return token

    def generate_token(self, connection_info):
        end_point = Endpoints.SESSIONS
        try:
            response = self._make_request(
                connection_info=connection_info,
                method="POST",
                end_point=end_point,
                data=None,
            )
            logger.writeDebug("generate_token response = {}", response)
        except Exception as e:
            logger.writeException(e)
            err_msg = (
                "Failed to establish a connection, please check the Management System address or the credentials."
                + str(e)
            )
            raise Exception(err_msg)

        session_id = response.get(API.SESSION_ID)
        token = response.get(API.TOKEN)
        logger.writeDebug(
            "generate_token session id = {} token = {}", session_id, token
        )
        return token

    def _make_request(self, connection_info, method, end_point, data=None):

        url = f"https://{connection_info.address}/ConfigurationManager/" + end_point
        logger.writeDebug("url = {}", url)

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        if data is not None:
            data = json.dumps(data)

        logger.writeDebug("method = {}", method)
        logger.writeDebug("headers = {}", headers)

        MAX_TIME_OUT = 300

        try:
            response = open_url(
                url=url,
                method=method,
                headers=headers,
                data=data,
                use_proxy=False,
                timeout=MAX_TIME_OUT,
                url_username=connection_info.username,
                url_password=connection_info.password,
                force_basic_auth=True,
                validate_certs=False,
            )
        except socket.timeout as t_err:
            logger.writeError(f"SessionManager._make_request - TimeoutError {t_err}")
            raise Exception(t_err)
        except urllib_error.HTTPError as err:
            logger.writeError(f"SessionManager._make_request - HTTPError {err}")

            if err.code == 503:
                # 503 Service Unavailable
                # wait for 5 mins and try to re-authenticate, we will retry 5 times
                if self.retry_count < 5:
                    logger.writeDebug(
                        "wait for 5 mins and try to generate session token again."
                    )
                    time.sleep(300)
                    self.retry_count += 1
                    return self._make_request(connection_info, method, end_point, data)
                else:
                    if hasattr(err, "read"):
                        error_resp = json.loads(err.read().decode())
                        logger.writeDebug(
                            f"SessionManager.error_resp - error_resp {error_resp}"
                        )
                        error_dtls = (
                            error_resp.get("message")
                            if error_resp.get("message")
                            else error_resp.get("errorMessage")
                        )
                        if error_resp.get("cause"):
                            error_dtls = error_dtls + " " + error_resp.get("cause")

                        if error_resp.get("solution"):
                            error_dtls = error_dtls + " " + error_resp.get("solution")

                        raise Exception(error_dtls)
            raise Exception(err)
        except Exception as err:
            logger.writeException(err)
            raise err

        if response.status not in (200, 201, 202):
            error_msg = json.loads(response.read())
            logger.writeError("error_msg = {}", error_msg)
            raise Exception(error_msg, response.status)

        return self._load_response(response)

    def _load_response(self, response):
        """returns dict if json, native string otherwise"""
        try:
            text = response.read().decode("utf-8")
            if "token" not in text:
                logger.writeDebug(f"{text[:5000]} ...")
            msg = {}
            raw_message = json.loads(text)
            if not len(raw_message):
                if raw_message.get("errorSource"):
                    msg[API.CAUSE] = raw_message[API.CAUSE]
                    msg[API.SOLUTION] = raw_message[API.SOLUTION]
                    return msg
            return raw_message
        except ValueError:
            return text
