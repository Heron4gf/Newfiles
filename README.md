# Newfiles

Newfiles is a Python application that monitors a directory for newly created files and automatically generates content for them using OpenAI's API. It supports different file types with customizable prompts and models.

## Features

- Monitors a directory for new file creations
- Generates content automatically based on file extension
- Supports both static and dynamic prompts
- Configurable models and settings per file extension
- Delay mechanism to prevent conflicts with other programs
- Subdirectory monitoring option

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd newfiles
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   - Rename `.env.example` to `.env`
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

## Configuration

The application can be configured through `config/config.json`:

- `monitored_directory`: The directory to monitor for new files
- `delay`: Delay in seconds before processing new files
- `monitor_subdirectories`: Whether to monitor subdirectories
- `default_text_prompt_file`: Default prompt file for text files
- `default_image_prompt_file`: Default prompt file for image files
- `extension_settings`: Extension-specific settings including model and prompt file

## Usage

### Command Line Version
Run the application with:
```
python main.py
```

Optional arguments:
- `--config`: Path to configuration file (default: config/config.json)
- `--directory`: Directory to monitor (overrides config)

### GUI Version
Run the GUI application with:
```
python newfiles_gui.py
```

The GUI version provides a user-friendly interface for:
- Selecting the monitored directory
- Configuring AI models for different file extensions
- Starting and stopping the monitoring service
- Viewing application logs

The new GUI version uses CustomTkinter for a more modern and visually appealing interface.

### Windows Service
For continuous background operation, you can run the application as a Windows service:
```
python windows_service.py
```

## Creating an Installer

To create a standalone Windows installer for the GUI application:

1. Install PyInstaller:
   ```
   pip install pyinstaller
   ```

2. Create the executable:
   ```
   pyinstaller newfiles.spec
   ```

3. Use Inno Setup to create an installer:
   - Download and install Inno Setup
   - Create a new script using the included files in the `dist/` folder
   - Configure desktop and start menu shortcuts
   - Compile the installer

## How it works

1. The application monitors the configured directory for new file creations
2. When a new file is detected, it waits for the configured delay
3. Based on the file extension, it determines the appropriate model and prompt
4. For text files, it can use dynamic prompts by referencing other files of the same type in the directory
5. It generates content using OpenAI's API and writes it to the new file

## Supported File Types

- Text files (.txt, .md, .py, .java, etc.)
- Image files (.png, .jpg, .jpeg)

## Customization

- Modify prompts in the `prompts/` directory
- Adjust extension settings in `config/config.json`
- Change monitoring settings in `config/config.json`

## Logging

Application logs are stored in `logs/newfiles.log`.
