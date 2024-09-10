import os
import sys
import speech_recognition as sr
import picamera
import sx126x
import termios
import tty

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

def send_message(node, message):
    """Send a message via LoRa."""
    offset_frequency = 868 - 850
    data = (
        bytes([0]) + 
        bytes([0]) + 
        bytes([offset_frequency]) + 
        bytes([node.addr >> 8]) + 
        bytes([node.addr & 0xff]) + 
        bytes([node.offset_freq]) + 
        message.encode()
    )
    node.send(data)

def main():
    """Main function to handle speech recognition and image capturing."""
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())

    node = setup_loRa()
    desktop_path = "/home/raspberry/Desktop/IoT Project"
    r = sr.Recognizer()

    with sr.Microphone(sample_rate=44100, chunk_size=1024) as source:
        r.adjust_for_ambient_noise(source)
        print("Say 'capture' to take a picture...")

        while True:
            try:
                audio = r.listen(source, timeout=None)
                words = r.recognize_google(audio)
                print("You said:", words)

                if "capture" in words.lower():
                    with picamera.PICamera() as camera:
                        image_path = os.path.join(desktop_path, "captured_image.jpg")
                        camera.capture(image_path)
                    print(f"Image captured and saved as '{image_path}'")
                    send_message(node, "Image captured")

            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                print("Google Web Speech API could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Web Speech API; {e}")

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

if __name__ == "__main__":
    main()
