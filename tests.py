from typing import Any

from dataclasses import dataclass, field

@dataclass
class Message:
    id:str
    sensor_model:str
    payloads: Any
    decoded_payload:Any = field(init=False)
    

CONFIGURATIONS = {
    "WS-0001": {
        "outputs": [{"type": "file", "config": {"path": "./logs/WS-0001.log."}}],
        "decoders": [
            {"type": "hex", "config": {}},
            {"type": "bytes", "config": {"payload_encoding": "UTF-8"}},
            {"type": "sep", "config": {"separator": "/"}},
        ],
    },
    "WS-0002": {
        "outputs": [{"type": "file", "config": {"path": "./logs/WS-0002.log."}}],
        "decoders": [{"type": "sep", "config": {"separator": "/"}}],
    },
    "WS-0003": {
        "outputs": [{"type": "file", "config": {"path": "./logs/WS-0003.log."}}],
        "decoders": [
            {"type": "base64", "config": {}},
            {"type": "bytes", "config": {"payload_encoding": "UTF-8"}},
        ],
    },
}

m0 = Message("123134", "ws01", "sadd213")



class Processor(ABC):
    @abstractmethod
    def process(self, entity: Any) -> Any:
        pass
    
    

class MessageProcessor(Processor):
    def process(self, entity: Message) -> Message:
        """Outputs the updated messages dict with an extra field
        named 'decoded_payload', decode_separated_sensor is used for
        decoding.
        :argument entity - messages to update
        """
        writers = []
        decoders = []
        decoded_payload = entity.payload
        config = CONFIGURATIONS.get(entity.sensor_model)

        try:
            for decoder in config.get("decoders"):
                decoders.append(get_decoder_implementation(decoder))
        except ValueError as e:
            print(e)
            raise e

        try:
            for wr in config.get("outputs"):
                writers.append(get_writer_implementation(wr))
        except ValueError as e:
            print(e)
            raise e

        try:
            for decoder in decoders:
                decoded_payload = decoder.decode_payload(decoded_payload)
                entity.decoded_payload = decoded_payload

            for writer in writers:
                writer.write(entity.decoded_payload)
        except Exception as e:
            print(e)
            raise e
        return entity