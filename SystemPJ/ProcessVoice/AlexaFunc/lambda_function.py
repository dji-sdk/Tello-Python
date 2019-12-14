# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import boto3
import json
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.utils import is_intent_name, get_dialog_state, get_slot_value
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
iot = boto3.client('iot-data')

def publish(msg):
    # ⑤トピックを指定
    topic = 'test/pub'
    # ⑥メッセージの内容
    payload = {
        "message": msg
    }  

    try:
        # ⑦メッセージをPublish
        iot.publish(
            topic=topic,
            qos=0,
            payload=json.dumps(payload, ensure_ascii=False)
        )
        return True
    
    except Exception as e:
        print(e)
        return False


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "離陸します"
        if publish("takeoff"):
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .ask("指示があればおっしゃってください。")
                    .response
            )
        else:
            return (
                handler_input.response_builder
                    .speak("エラー")
                    .response
            )


class ControllerHandler(AbstractRequestHandler):
    """Handler for Controller."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("Controller")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        slots = handler_input.request_envelope.request.intent.slots

        if "direction" in session_attr: # 初回以降のコントローラー呼び出し
            if get_slot_value(handler_input=handler_input, slot_name="direction"): # 方向を入力した場合
                direction = slots["direction"].resolutions.resolutions_per_authority[0].values[0].value.name
                direction_id = slots["direction"].resolutions.resolutions_per_authority[0].values[0].value.id
            elif session_attr["direction"]: # すでに方向を入力していた場合
                direction = session_attr["direction"]
                direction_id = session_attr["direction_id"]
            else: # 方向を入力していない場合
                direction = None
        else: # 初回のコントローラー呼び出し
            if get_slot_value(handler_input=handler_input, slot_name="direction"): # 方向を入力した場合
                direction = slots["direction"].resolutions.resolutions_per_authority[0].values[0].value.name
                direction_id = slots["direction"].resolutions.resolutions_per_authority[0].values[0].value.id
            else: # 方向を入力しなかった場合
                direction = None
            
        if "num" in session_attr: # 初回以降のコントローラー呼び出し
            num = get_slot_value(handler_input=handler_input, slot_name="num") or session_attr["num"]
        else: # 初回のコントローラー呼び出し
            num = get_slot_value(handler_input=handler_input, slot_name="num")


        if not direction:
            session_attr["num"] = num
            speak_output = "どちらに向かいますか？"
            reprompt = "どちらに向かいますか？"
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .ask(reprompt)
                    .response
            )
        if not num:
            session_attr["direction"] = direction
            session_attr["direction_id"] = direction_id
            speak_output = "何センチ移動しますか？"
            reprompt = "何センチ移動しますか？"
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .ask(reprompt)
                    .response
            )

        session_attr['direction'] = None
        session_attr['direction_id'] = None
        session_attr['num'] = None
        speak_output = f"{num}センチ、{direction}に移動します。"
        if publish(f"{direction_id} {num}"):
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .ask("どうしますか？")
                    .response
            )
        else:
            return (
                handler_input.response_builder
                    .speak("通信エラーがおきました。")
                    # .ask("add a reprompt if you want to keep the session open for the user to respond")
                    .response
            )

class LandHandler(AbstractRequestHandler):
    """Handler for Controller."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("Land")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "着陸します"

        if publish("land"):
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .response
            )
        else:
            return (
                handler_input.response_builder
                    .speak("通信エラーがおきました。")
                    .response
            )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "ドローンを飛ばす方向と距離をセンチで教えて下さい。"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "エラーがおきたよ"

        if publish("land"):
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .response
            )
        else:
            return (
                handler_input.response_builder
                    .speak("通信エラーがおきました。")
                    .response
            )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ControllerHandler())
sb.add_request_handler(LandHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()