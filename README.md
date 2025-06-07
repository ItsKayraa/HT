# HT
HT is a basic compiler language which doesn't really have many librarys within it. It's open source and open for development. It has i686 and x86_64 support. NASM Assembler. It's made for only Linux Support.

## 📂 Requirements

To use HT Compiler you must have these:

1) Netwide Assembler
2) GNU Linker
3) Python 3.8+

## 📁 Installation

To install the package, you must clone the source code and set installation path on "htcompiler.py".

```bash
git clone https://github.com/ItsKayraa/HT
cd HT
```

After installing and navigating to HT path, edit the `htcompiler.py` file like this:

```python
htInstallPath = "/home/kayra/Projects/ht" # Change this with your installation path!!!
```

Make sure you did change it to your installation path. (I will make a sh file for this soon.)

After everything is done, you must be able to use it!

## ✅ Usage

To use HT Compiler, you must make sure you did do the instructions in the **Installation** part.

After you have done the installation, now you can use it freely! To compile an HT file you must use these commands:

```bash
python3 htcompiler.py yourhtfile.ht yourhtfileoutput -o1
# -o1 = Output will be first arguement after the file / If not given it will be file.removesuffix(".ht")
# -b32 = 32 Bits version (must use 32 bit librarys to work correctly)
# -kt / --keeptemp = Keep temporary files which will be removed already.
```

You have compiled your first HT file now!

## ❔ Syntax

For syntax, read syntax.txt

(Hey, this is one of my first github projects! Please do not hate me if the README is bad...)
