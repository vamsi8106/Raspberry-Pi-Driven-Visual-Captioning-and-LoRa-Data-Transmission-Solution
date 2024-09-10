# Raspberry Pi-Driven Visual Captioning and LoRa Data Transmission Solution

## Project Overview

This project presents an advanced IoT system that integrates a Raspberry Pi Model 4B, LoRa communication technology, and a microphone to create a sophisticated solution for real-time image caption generation, data transmission, and auditory feedback. The system seamlessly combines image analysis with auditory output, transforming visual information into actionable audio feedback.

## Workflow of the Project

### Node Setup

#### Node Configuration
- **Node-1 (Transmitter):** 
  - Equipped with a Raspberry Pi Model 4B, Pi-camera, and a microphone. 
  - Responsible for capturing images, generating captions, and transmitting data.
- **Node-2 (Receiver):**
  - Also utilizes a Raspberry Pi Model 4B with LoRa hat components for receiving and processing transmitted information.

#### LoRa Communication
- Each node is assigned a unique address, with Node-1 functioning as the transmitter and Node-2 as the receiver.
- The LoRa hat components enable long-range communication between the two nodes.

### Image Capture and Captioning

#### Speech Trigger
- At Node-1, the system listens for the keyword "capture" through the connected microphone.

#### Image Capture
- Upon detecting the keyword, Node-1 activates the Pi-camera to capture an image.

#### Image Processing
- The captured image is processed on Node-1 using a pre-trained VGGNet model. This model generates a caption describing the contents of the image.

#### Caption Transmission
- The generated caption is transmitted from Node-1 to Node-2 using LoRa communication.

### Audio Feedback

#### Caption Reception
- At Node-2, the received caption string is extracted from the data.

#### Audio Conversion
- The caption string is then converted into an audio file in .mp3 format.

#### Audio Playback
- The audio file is played back in real time through headphones or other audio output devices, including wired or Bluetooth speakers.

## Applications

This project has significant potential for a variety of practical applications:

- **Remote Surveillance:** Provides real-time insights by analyzing captured images and conveying relevant information through audio feedback.
- **Assistance for Individuals with Visual Impairments:** Converts image information into audio, assisting users in interpreting their surroundings.

## Getting Started

1. **Hardware Requirements:**
   - Two Raspberry Pi Model 4B boards
   - LoRa hat components
   - Pi-camera
   - Microphone
   - Audio output devices (headphones, wired or Bluetooth speakers)

2. **Software Requirements:**
   - Pre-trained VGGNet model for image captioning
   - LoRa communication libraries and drivers

3. **Setup Instructions:**
   - Configure Node-1 with Pi-camera and microphone.
   - Install and configure LoRa communication components.
   - Deploy the VGGNet model on Node-1 for image captioning.
   - Set up Node-2 to receive and process data from Node-1.

4. **Running the System:**
   - Ensure both nodes are powered and connected.
   - Node-1 will capture images and send captions upon detecting the keyword "capture."
   - Node-2 will receive the captions, convert them to audio, and playback in real-time.
  
## Running the System

To run the system, follow these steps:

1. **On Transmitter Node (Node-1):**
   - Execute the transmitter script to start capturing images and sending captions.
   - Run the following command:
     ```bash
     python3 main_transmitter.py
     ```

2. **On Receiver Node (Node-2):**
   - Execute the receiver script to start receiving captions and converting them to audio.
   - Run the following command:
     ```bash
     python3 main_receiver.py
     ```

## Conclusion

This project demonstrates the effective integration of IoT technologies for real-time image captioning and auditory feedback, offering practical solutions for remote surveillance and assistance for individuals with visual impairments.
