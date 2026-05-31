# XenHide a tool for Steganography
## Status:Early-Development 
This is my attempt to learn amazing tools like `steghide`, `zsteg`, etc.

## Steganography

Steganography is the practice of hiding information within another medium in such a way that the existence of the hidden information itself is concealed.
The key idea is subtlety: the carrier appears normal to an observer, while only the intended recipient knows that hidden information exists and how to extract it.

## Steganography in the Digital Context

In the digital world, steganography commonly involves embedding data inside digital files such as images, audio, video, or even network packets. For example:

- Hiding text inside the least significant bits (LSB) of an image’s pixels  
- Embedding data inside audio waveforms without perceptible distortion  
- Concealing information within metadata or file structure patterns  


## Current implementation

- inspired by tools such as `steghide` and `zsteg`.
- Simple command-line scripts: `xencrypt.py`, `xendcrypt.py`.
- A lightweight GUI prototype in `Application/XenHideGUI.py`.

## Getting Started
requirements
- Python 3.x (i used 3.13)
- stegano
- PyQt5 (GUI)

Quick install

1. Clone the repository or copy the project files.
2. (Optional) Create and activate a virtual environment:

	python -m venv .venv
	source .venv/bin/activate
    

3. Install any dependencies if needed (this project is mostly self-contained).

Running the examples

- Command line encrypt: `python xencrypt.py` (see script for options)
- Command line decrypt: `python xendcrypt.py`
- GUI: `python Application/XenHideGUI.py`

## Files
- `xencrypt.py` — simple embedding example
- `xendcrypt.py` — extraction/decode example
- `Application/XenHideGUI.py` — experimental GUI frontend

## Contributing
Contributions, issues, and suggestions are welcome. This project is intended for learning — be mindful of legal and ethical considerations when working with steganography.

``` License```
This project is released under the GNU General Public License v3.0. See the `LICENSE` file for details.

```Reference:``` ![Wikipedia–Steganography](https://en.wikipedia.org/wiki/Steganography)

---