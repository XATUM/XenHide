# XenHide

XenHide is a Python-based steganography toolkit for embedding and extracting hidden data within digital media. It provides both command-line scripts and a lightweight graphical interface, inspired by tools such as `steghide` and `zsteg`.

XenHide runs on Linux, Windows, and macOS.

## Table of Contents

- [What is Steganography?](#what-is-steganography)
- [Building](#building)
- [Usage](#usage)
- [Installation](#install)
- [Contributing](#contributing)
- [Security & Ethics](#security--ethics)

## What is Steganography?

Steganography is the practice of concealing information within a non-secret carrier medium such that the existence of the hidden data is not apparent to an observer. Unlike encryption, which makes data unreadable, steganography makes data invisible.

In the digital world, common techniques include:

- Hiding text inside the least significant bits (LSB) of an image's pixels
- Embedding data inside audio waveforms without perceptible distortion
- Concealing information within metadata or file structure patterns

XenHide currently focuses on image-based steganography using the LSB technique.

## Building

XenHide is a Python project with minimal dependencies. A virtual environment is recommended.

### Requirements

| Platform      | Dependencies              |
|---------------|---------------------------|
| Linux         | Python 3.13+, stegano       |
| Windows       | Python 3.13+, stegano       |
| macOS         | Python 3.13+, stegano       |
| GUI (all)     | PyQt5 (optional)          |

Developed and tested on Python 3.13.

## Install
Download the latest version from the [XenHide Releases](https://github.com/XATUM/XenHide/releases) 

linux:(still working)
### Linux / macOS

```
git clone https://github.com/XATUM/XenHide.git
cd XenHide
python -m venv .venv
source .venv/bin/activate
pip install stegano PyQt5
```

### Windows

```
git clone https://github.com/XATUM/XenHide.git
cd XenHide
python -m venv .venv
.venv\Scripts\activate
pip install stegano PyQt5
```

## Usage

### Command Line

Embed data into an image:

```
python xencrypt.py
```

Extract hidden data from an image:

```
python xendcrypt.py
```

See each script's inline comments for available options.

### Graphical Interface

```
python Application/XenHideGUI.py
```

### Project Files

```
XenHide/
├── xencrypt.py            — CLI tool for embedding data into a carrier image
├── xendcrypt.py           — CLI tool for extracting hidden data from an image
├── Application/
│   └── XenHideGUI.py      — Experimental PyQt5 graphical frontend
└── LICENSE
```

## Contributing

Contributions, bug reports, and feature suggestions are welcome. Please open an issue before submitting a pull request so the change can be discussed first.

To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a pull request

This project is intended for learning and authorized research. Please be mindful of the legal and ethical implications when working with steganography.

## Security & Ethics

XenHide is intended strictly for educational purposes, authorized security research, and lawful use cases. Users are responsible for ensuring their use of this tool complies with applicable laws and regulations.

## License

This project is released under the GNU General Public License v3.0. See the `LICENSE` file for details.

## References

- [Wikipedia — Steganography](https://en.wikipedia.org/wiki/Steganography)
- [steghide](https://steghide.sourceforge.net/)
- [zsteg](https://github.com/zed-0xff/zsteg)
- [stegano](https://pypi.org/project/stegano/)
