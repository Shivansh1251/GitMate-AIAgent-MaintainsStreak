# GitMate-AIAgent-MaintainsStreak

> An automated daily Git uploader to maintain your GitHub contribution streak

GitMate is a Python-based automation tool that helps you maintain your GitHub contribution streak by automatically uploading files from your local sources to a GitHub repository on a schedule. Perfect for developers who want to ensure consistent daily commits without manual intervention.

## 🌟 Features

- **Automated Daily Uploads**: Automatically selects and uploads files from your source directory
- **Multiple Upload Strategies**: Choose between rotate, random, or single file selection
- **Flexible Authentication**: Supports both SSH and HTTPS authentication methods
- **Smart File Management**: Prevents overwrites with timestamp-based naming
- **State Persistence**: Tracks upload history and maintains day count
- **Dry Run Mode**: Test your configuration without actual commits
- **Configurable**: Highly customizable through YAML configuration

## 🚀 Quick Start

### Prerequisites

- Python 3.6+
- Git installed and configured
- GitHub repository (public or private)
- SSH key configured (recommended) or GitHub token for HTTPS

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Shivansh1251/GitMate-AIAgent-MaintainsStreak.git
   cd GitMate-AIAgent-MaintainsStreak
   ```

2. Install required dependencies:
   ```bash
   pip install pyyaml
   ```

3. Configure your settings in `config.yaml` (see Configuration section below)

4. Run the tool:
   ```bash
   python main.py
   ```

## ⚙️ Configuration

Create or modify `config.yaml` with your settings:

```yaml
# Local path where the repository will be cloned/managed
repo_local_path: D:/GitMate-AIAgent-MaintainsStreak/repo

# GitHub repository URL (SSH recommended)
repo_remote: git@github.com:yourusername/your-repo.git

# Target branch (usually 'main' or 'master')
branch: main

# Source files/directories to upload from
source_paths:
  - D:\path\to\your\sources\file1.html
  - D:\path\to\your\sources\file2.txt

# Upload strategy: 'rotate', 'random', or 'single'
upload_strategy: rotate

# Destination folder within the repository
dest_subfolder: uploads

# Commit message template
commit_message_template: "Day {day}: Added {name} (auto by GitMate)"

# Authentication method: 'ssh' or 'https'
auth_method: ssh

# SSH private key path (if using SSH auth)
ssh_key_path: /path/to/your/.ssh/id_ed25519
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `repo_local_path` | Local directory for repository clone | Required |
| `repo_remote` | GitHub repository URL | Required |
| `branch` | Target branch name | `main` |
| `source_paths` | List of files/directories to upload | Required* |
| `source_dir` | Single directory to pick files from | Required* |
| `upload_strategy` | File selection strategy | `rotate` |
| `dest_subfolder` | Upload destination within repo | `uploads` |
| `commit_message_template` | Template for commit messages | `Day {day}: {name}` |
| `auth_method` | Authentication method | `ssh` |
| `ssh_key_path` | Path to SSH private key | Optional |

*Either `source_paths` or `source_dir` must be specified

## 🔄 Upload Strategies

- **`rotate`**: Cycles through source files in order
- **`random`**: Randomly selects a file each time
- **`single`**: Always uploads the first file in the list

## 🛠️ Usage

### Basic Usage
```bash
python main.py
```

### With Custom Config
```bash
python main.py --config /path/to/your/config.yaml
```

### Dry Run (Test Mode)
```bash
python main.py --dry-run
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `--config`, `-c` | Path to configuration file |
| `--dry-run` | Test run without actual commits/pushes |

## 📁 Project Structure

```
GitMate-AIAgent-MaintainsStreak/
├── main.py              # Main application script
├── config.yaml          # Configuration file
├── state.json           # Persistent state storage
├── README.md            # This file
├── .gitignore          # Git ignore rules
├── sources/            # Source files directory
│   ├── index.html
│   ├── initials.jpg
│   └── ...
└── repo/               # Cloned repository (auto-created)
    └── uploads/        # Uploaded files destination
```

## 🔐 Authentication Setup

### SSH (Recommended)

1. Generate SSH key (if not already done):
   ```bash
   ssh-keygen -t ed25519 -C "your-email@example.com"
   ```

2. Add public key to GitHub (Settings → SSH and GPG keys)

3. Update `config.yaml` with your SSH key path

### HTTPS with Token

1. Create a Personal Access Token on GitHub
2. Set the `GITHUB_TOKEN` environment variable
3. Use HTTPS URL in `repo_remote`
4. Set `auth_method: https` in config

## 🤖 Automation

### Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., daily at specific time)
4. Set action to start program: `python`
5. Add arguments: `path\to\main.py`
6. Set start in: `path\to\GitMate-AIAgent-MaintainsStreak`

### Linux/macOS Cron

Add to crontab (`crontab -e`):
```bash
# Run daily at 9 AM
0 9 * * * cd /path/to/GitMate-AIAgent-MaintainsStreak && python main.py
```

## 📊 State Management

GitMate maintains state in `state.json`:
```json
{
  "last_index": 0,
  "day_count": 1
}
```

- `last_index`: Index of last uploaded file (for rotation)
- `day_count`: Number of successful uploads

## 🐛 Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Verify SSH key is added to GitHub
   - Check SSH key permissions (`chmod 600 ~/.ssh/id_ed25519`)
   - Test SSH connection: `ssh -T git@github.com`

2. **No Source Files Found**
   - Check `source_paths` in config.yaml
   - Ensure file paths exist and are accessible
   - Use absolute paths to avoid confusion

3. **Git Operations Fail**
   - Ensure Git is installed and in PATH
   - Verify repository URL is correct
   - Check network connectivity

### Debug Mode

Run with verbose output:
```bash
python main.py --dry-run
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## �‍💻 Made by

**Shivansh** - [@Shivansh1251](https://github.com/Shivansh1251)

Feel free to reach out if you have any questions or suggestions!

## �📄 License

This project is open source and available under the [MIT License](LICENSE).

## ⭐ Support

If GitMate helps you maintain your GitHub streak, please consider:
- Starring this repository
- Sharing it with fellow developers
- Contributing improvements

---

**Happy Coding!** 🚀