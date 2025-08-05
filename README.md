# Newfiles 📄✨

[![License](https://img.shields.io/github/license/Heron4gf/Newfiles)](https://github.com/Heron4gf/Newfiles/blob/main/LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/Heron4gf/Newfiles)](https://github.com/Heron4gf/Newfiles/commits/main)
![Repo Top Language](https://img.shields.io/github/languages/top/Heron4gf/Newfiles)
[![Language Count](https://img.shields.io/github/languages/count/Heron4gf/Newfiles)](https://github.com/Heron4gf/Newfiles)

Newfiles is an intelligent file monitoring application that automatically generates content for newly created files using AI. Say goodbye to empty files and hello to AI-powered productivity!

https://github.com/Heron4gf/Newfiles/assets/12345678/placeholder-demo.gif

## 🌟 Why Newfiles?

Tired of staring at blank files? Newfiles solves this by automatically filling your new files with relevant content based on their names and extensions. Whether you're creating a Python script, a Markdown document, or even requesting an image, Newfiles has you covered with AI-generated content.

## 🚀 Key Features

- **Smart File Monitoring**: Automatically detects new files in your specified directory
- **AI-Powered Content Generation**: Uses OpenAI's advanced models to create relevant content
- **Multi-Format Support**: Works with text files (.txt, .md, .py, .java) and images (.png, .jpg)
- **Customizable Prompts**: Tailor the AI's behavior with your own prompt templates
- **Flexible Configuration**: Adjust settings for different file types and monitoring preferences
- **Beautiful GUI**: Modern interface built with CustomTkinter for easy configuration
- **Background Service**: Run continuously in the background as a Windows service
- **Dynamic Prompts**: For text files, the AI can reference existing files in the same directory

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Heron4gf/Newfiles.git
   cd Newfiles
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   Create a `.env` file in the root directory with your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

## ⚙️ Configuration

The application can be configured through `config/config.json`:

- `monitored_directory`: The directory to monitor for new files
- `delay`: Delay in seconds before processing new files
- `monitor_subdirectories`: Whether to monitor subdirectories
- `default_text_prompt_file`: Default prompt file for text files
- `default_image_prompt_file`: Default prompt file for image files
- `extension_settings`: Extension-specific settings including model and prompt file

## 🖥️ Usage

### Command Line Version
Run the application with:
```bash
python main.py
```

Optional arguments:
- `--config`: Path to configuration file (default: config/config.json)
- `--directory`: Directory to monitor (overrides config)

### GUI Version
Run the GUI application with:
```bash
python newfiles_gui.py
```

The GUI version provides a user-friendly interface for:
- Selecting the monitored directory
- Configuring AI models for different file extensions
- Starting and stopping the monitoring service
- Viewing application logs

### Windows Service
For continuous background operation, you can run the application as a Windows service:
```bash
python windows_service.py
```

## 🛠️ Creating an Installer

To create a standalone Windows installer for the GUI application:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Create the executable:
   ```bash
   pyinstaller newfiles.spec
   ```

3. Use Inno Setup to create an installer:
   - Download and install Inno Setup
   - Create a new script using the included files in the `dist/` folder
   - Configure desktop and start menu shortcuts
   - Compile the installer

## 🧠 How It Works

1. The application monitors the configured directory for new file creations
2. When a new file is detected, it waits for the configured delay
3. Based on the file extension, it determines the appropriate model and prompt
4. For text files, it can use dynamic prompts by referencing other files of the same type in the directory
5. It generates content using OpenAI's API and writes it to the new file

## 📝 Supported File Types

- Text files (.txt, .md, .py, .java, etc.)
- Image files (.png, .jpg, .jpeg)

## 🎨 Customization

- Modify prompts in the `prompts/` directory
- Adjust extension settings in `config/config.json`
- Change monitoring settings in `config/config.json`

## 📋 Logging

Application logs are stored in `logs/newfiles.log`.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
