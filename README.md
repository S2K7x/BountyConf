# BountyConf

BountyConf.py is an automated setup script for bug bounty hunters and security researchers. It installs, configures, and organizes essential tools for reconnaissance, enumeration, and vulnerability scanning.

## Features

- **Automated environment setup**: Creates an organized structure for bug bounty tools.
- **Dependency management**: Installs required packages (Python, Go, Ruby, Java, Git, etc.).
- **Tool installation**:
  - **APT Tools**: nmap, dnsutils
  - **Go Tools**: Amass, Subfinder, Assetfinder, FFUF, Gobuster, etc.
  - **Manual Tools**: Sublist3r, LinkFinder, DNSRecon, EyeWitness, Masscan
  - **Pip Tools**: trufflehog, arjun
  - **Gem Tools**: whatweb
- **Wordlist management**: Clones SecLists and fetches additional useful wordlists.
- **Virtual environment support**: Creates a Python virtual environment for isolated tool execution.
- **Update mechanism**: Automatically updates installed tools when the script is re-run.

## Installation

Ensure you have `Python3` installed. Verify with:

```bash
python3 --version
```

Then, clone this repository and navigate to the directory:

```bash
git clone https://github.com/s2k7x/BountyConf.git
cd BountyConf
```

## Usage

Run the script to set up your environment:

```bash
python3 BountyConf.py
```

## Directory Structure

After running the script, your environment will be organized as follows:

```
bugbounty_tools/
├── venv/          # Virtual environment for pip tools
├── go/            # Go tools (binaries in go/bin/)
├── manual_tools/  # Manually cloned tools
├── wordlists/     # Useful wordlists (SecLists, all.txt)
```

## Using Installed Tools

### Python Virtual Environment

Activate the virtual environment and run pip-based tools:

```bash
source bugbounty_tools/venv/bin/activate
trufflehog --help
```

### Go Tools

Add Go tools to your PATH or run them directly:

```bash
export PATH=$PATH:$(pwd)/bugbounty_tools/go/bin
amass --help
```

### Manual Tools

Navigate to the respective tool's directory and install dependencies if needed:

```bash
cd bugbounty_tools/manual_tools/Sublist3r
pip install -r requirements.txt
python sublist3r.py -h
```

### Wordlists

Use wordlists for fuzzing, brute-force attacks, or subdomain enumeration:

```bash
cat bugbounty_tools/wordlists/all.txt | while read domain; do subfinder -d $domain; done
```

## Updating Tools

Re-run the script to fetch updates for installed tools:

```bash
python3 BountyConf.py
```

## Requirements

- Python 3.x
- sudo/root privileges (for APT and system-wide installations)
- Go installed (for Go-based tools)
- Internet connection (for downloading tools and wordlists)

## Contribution

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
