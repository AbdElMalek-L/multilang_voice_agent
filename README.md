# Multilingual Voice Agent

## Project Description

This project implements a multilingual voice agent capable of transcribing audio input, processing it with a Large Language Model (LLM), and generating an audio response using a Text-to-Speech (TTS) service. The agent leverages `fastrtc` for real-time communication, `ollama` for LLM integration, `whisper_stt` for Speech-to-Text, and `kokoro_tts` for Text-to-Speech.

## Features

- **Real-time Audio Processing**: Utilizes `fastrtc` for efficient real-time audio input and output.
- **Multilingual Speech-to-Text (STT)**: Transcribes user's speech into text using `faster_whisper`.
- **Large Language Model (LLM) Integration**: Processes transcribed text and generates intelligent responses using `ollama`.
- **Text-to-Speech (TTS)**: Synthesizes LLM responses into natural-sounding speech using `kokoro_tts`.
- **Chat History Management**: Maintains conversation context to enable more coherent and continuous interactions.
- **Command-line Arguments**: Configurable STT and TTS providers, and voice ID through command-line arguments.
- **UI Options**: Supports both FastRTC phone interface and Gradio UI for interaction.

## Installation

### Prerequisites

- Python 3.9+
- `ollama` installed and running for the LLM service.

### Steps

1.  **Clone the repository**:

    ```bash
    git clone <repository_url>
    cd multilang_voice_agent
    ```

2.  **Create a virtual environment** (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables**:

    Create a `.env` file in the root directory and add the following:

    ```
    TTS_PROVIDER=kokoro
    STT_PROVIDER=whisper
    VOICE_ID=en_US # Example for Kokoro TTS, adjust as needed
    OLLAMA_BASE_URL=http://localhost:11434 # Or your Ollama server address
    LLM_MODEL=gemma:1b # Or your preferred Ollama model
    ```

    *Note: Ensure your `ollama` server is running and the specified `LLM_MODEL` is available.*

## Usage

To run the voice agent, execute the `main.py` file. You can specify various options using command-line arguments:

```bash
python main.py --help
```

### Examples

- **Launch with Gradio UI (default)**:

    ```bash
    python main.py
    ```

- **Launch with FastRTC phone interface**:

    ```bash
    python main.py --phone
    ```

- **Specify TTS and STT providers**:

    ```bash
    python main.py --tts kokoro --stt whisper
    ```

- **Specify a voice ID**:

    ```bash
    python main.py --voice <your_voice_id>
    ```

## Project Structure

```
. # Project Root
├── config/
├── main.py                 # Main entry point and FastRTC stream setup
├── requirements.txt        # Python dependencies
└── src/
    ├── __init__.py
    ├── agent.py              # Orchestrates STT, LLM, and TTS interactions
    ├── chat_history.py       # Manages conversation history
    ├── llm_service.py        # Handles interactions with the Large Language Model
    ├── speech/
    │   ├── stt/
    │   │   ├── __init__.py
    │   │   ├── provider.py   # Base class for STT providers
    │   │   └── whisper_stt.py  # Whisper STT implementation
    │   └── tts/
    │       ├── __init__.py
    │       ├── kokoro_tts.py   # Kokoro TTS implementation
    │       └── provider.py   # Base class for TTS providers
    └── tools/                  # Placeholder for future tools/utilities
```

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License.
