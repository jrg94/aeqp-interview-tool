Ran into an error with the installation of pyaudio:

```
Collecting pyaudio
  Using cached https://files.pythonhosted.org/packages/ab/42/b4f04721c5c5bfc196ce156b3c768998ef8c0ae3654ed29ea5020c749a6b/PyAudio-0.2.11.tar.gz
Installing collected packages: pyaudio
  Running setup.py install for pyaudio: started
    Running setup.py install for pyaudio: finished with status 'error'
    Complete output from command E:\Projects\EDAAudioSync\venv\Scripts\python.exe -u -c "import setuptools, tokenize;__file__='C:\\Users\\JEREMY~1\\AppData\\Local\\Temp\\pycharm-packaging\\pyaudio\\setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" install --record "C:\Users\Jeremy Grifski\AppData\Local\Temp\pip-record-cg4mrjiy\install-record.txt" --single-version-externally-managed --compile --install-headers E:\Projects\EDAAudioSync\venv\include\site\python3.8\pyaudio:
    running install
    running build
    running build_py
    creating build
    creating build\lib.win32-3.8
    copying src\pyaudio.py -> build\lib.win32-3.8
    warning: build_py: byte-compiling is disabled, skipping.

    running build_ext
    building '_portaudio' extension
    error: Microsoft Visual C++ 14.0 is required. Get it with "Microsoft Visual C++ Build Tools": https://visualstudio.microsoft.com/downloads/

    ----------------------------------------
```