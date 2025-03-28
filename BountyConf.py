import os
import subprocess
import shutil

def run_command(command, env=None, cwd=None):
    """Run a shell command and handle errors."""
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(command)}: {e}")

# Main directory for all bug bounty tools
main_dir = "bugbounty_tools"

# Create main directory and subdirectories
print("Setting up directory structure...")
for subdir in [main_dir, os.path.join(main_dir, "venv"), os.path.join(main_dir, "go"), 
               os.path.join(main_dir, "manual_tools"), os.path.join(main_dir, "wordlists")]:
    os.makedirs(subdir, exist_ok=True)

# Check and install essential dependencies
print("Checking and installing dependencies...")
dependencies = {
    "python3": "python3",
    "pip3": "python3-pip",
    "go": "golang",
    "ruby": "ruby",
    "java": "default-jdk",
    "git": "git"
}
for cmd, pkg in dependencies.items():
    if not shutil.which(cmd):
        print(f"{cmd} not found. Installing {pkg}...")
        run_command(["sudo", "apt", "install", "-y", pkg])

# Create virtual environment
print("Creating virtual environment...")
venv_path = os.path.join(main_dir, "venv")
run_command(["python3", "-m", "venv", venv_path])

# Install apt tools (system-wide)
print("Installing apt tools...")
apt_tools = ["nmap", "dnsutils"]
run_command(["sudo", "apt", "install", "-y"] + apt_tools)

# Install gem tools (system-wide)
print("Installing gem tools...")
gem_tools = ["whatweb"]
run_command(["gem", "install"] + gem_tools)

# Install Go tools into bugbounty_tools/go/bin
print("Installing Go tools...")
go_env = os.environ.copy()
go_env["GOPATH"] = os.path.abspath(os.path.join(main_dir, "go"))
go_tools = [
    "github.com/OWASP/Amass/v3/...@latest",
    "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
    "github.com/tomnomnom/assetfinder@latest",
    "github.com/lc/gau/v2/cmd/gau@latest",
    "github.com/ffuf/ffuf@latest",
    "github.com/OJ/gobuster/v3@latest",
    "github.com/tomnomnom/waybackurls@latest",
    "github.com/haccer/subjack@latest",
    "github.com/blechschmidt/massdns@latest",
    "github.com/gitleaks/gitleaks@latest"
]
for tool in go_tools:
    run_command(["go", "install", tool], env=go_env)

# Install manual tools via git clone into bugbounty_tools/manual_tools
print("Installing manual tools...")
manual_tools = {
    "Sublist3r": "https://github.com/aboul3la/Sublist3r.git",
    "LinkFinder": "https://github.com/GerbenJavado/LinkFinder.git",
    "DNSRecon": "https://github.com/darkoperator/dnsrecon.git",
    "EyeWitness": "https://github.com/FortyNorthSecurity/EyeWitness.git",
    "Masscan": "https://github.com/robertdavidgraham/masscan.git"
}
manual_tools_dir = os.path.join(main_dir, "manual_tools")
for tool, repo in manual_tools.items():
    tool_dir = os.path.join(manual_tools_dir, tool)
    if os.path.exists(tool_dir):
        print(f"Updating {tool}...")
        run_command(["git", "pull"], cwd=tool_dir)
    else:
        print(f"Cloning {tool}...")
        run_command(["git", "clone", repo, tool_dir])

# Install pip tools into the venv (dependencies included, but not requirements.txt)
print("Installing pip tools into venv...")
pip_tools = ["trufflehog", "arjun"]
venv_pip = os.path.join(venv_path, "bin", "pip")
run_command([venv_pip, "install", "--upgrade"] + pip_tools)

# Add useful wordlists
print("Downloading useful wordlists...")
wordlists_dir = os.path.join(main_dir, "wordlists")
if os.path.exists(os.path.join(wordlists_dir, "SecLists")):
    print("Updating SecLists...")
    run_command(["git", "pull"], cwd=os.path.join(wordlists_dir, "SecLists"))
else:
    print("Cloning SecLists...")
    run_command(["git", "clone", "https://github.com/danielmiessler/SecLists.git", 
                 os.path.join(wordlists_dir, "SecLists")])

# Download an additional useful wordlist
all_txt_url = "https://gist.githubusercontent.com/jhaddix/86a06c5dc309d08580a018c66354a056/raw/96f4e51d96b2203f19f6381c8c545b278eaa6ca3/all.txt"
run_command(["wget", all_txt_url, "-O", os.path.join(wordlists_dir, "all.txt")], 
            env=None if os.path.exists(os.path.join(wordlists_dir, "all.txt")) else None)

# Print usage instructions
print("""
Setup complete! Your bug bounty environment is organized in 'bugbounty_tools/':

- **Directory Structure:**
  - bugbounty_tools/
    - venv/          # Virtual environment for pip tools
    - go/            # Go tools (binaries in go/bin/)
    - manual_tools/  # Manually cloned tools
    - wordlists/     # Useful wordlists for bug bounty hunting

- **To Use the Tools:**
  - **Pip Tools**: Activate the venv and use tools like trufflehog, arjun:
source bugbounty_tools/venv/bin/activate
trufflehog --help

- **Manual Tools**: Navigate to their directories and install their requirements manually:
source bugbounty_tools/venv/bin/activate
cd bugbounty_tools/manual_tools/Sublist3r
pip install -r requirements.txt

Note: Some tools (e.g., Masscan, EyeWitness) require additional setup (e.g., `make` or running setup scripts).
- **Go Tools**: Add the Go binaries to your PATH or run them directly:
export PATH=$PATH:$(pwd)/bugbounty_tools/go/bin
amass --help

- **Wordlists**: Available in bugbounty_tools/wordlists/ (e.g., SecLists, all.txt)
- **Apt/Gem Tools**: Installed system-wide (e.g., nmap, whatweb)

- **Additional Notes:**
- For tools requiring API keys or further configuration (e.g., Amass, EyeWitness), refer to their documentation.
- Run this script again to update tools (e.g., `git pull` for manual tools, `go install @latest` for Go tools).
""")