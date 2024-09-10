import sys
import os
import sx126x
import termios
import tty
import time
from pydub import AudioSegment
from pydub.playback import play

def setup_loRa():
    """Setup and return the LoRa node."""
    return sx126x.sx126x(
        serial_num="/dev/ttyS0",
        freq=868,
        addr=0,
        power=22,
        rssi=True,
        air_speed=2400,
        relay=False
    )

def receive_message(node):
    """Receive a message via LoRa and return it."""
    data = node.receive()
    if data:
        message = data[6:].decode()  # Assuming message starts after the header
        return message
    return None

def text_to_audio(text, filename="output.mp3"):
    """Convert text to audio and save as .mp3 file."""
    from gtts import gTTS
    tts = gTTS(text)
    tts.save(filename)

def play_audio(filename):
    """Play an audio file."""
    audio = AudioSegment.from_mp3(filename)
    play(audio)

def main():
    """Main function to handle message reception and playback."""
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())

    node = setup_loRa()
    audio_file = "output.mp3"

    print("Waiting for messages...")

    while True:
        try:
            message = receive_message(node)
            if message:
                print(f"Received message: {message}")
                text_to_audio(message, audio_file)
                play_audio(audio_file)

        except KeyboardInterrupt:
            print("Exiting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

if __name__ == "__main__":
    main()
