rm -r build
rm -r dist
rm "FUNSC.spec"
rm "FUNSC --debug.spec"
mkdir dist
cd dist
mkdir assets
cd ../
curl -o "dist/assets/result.png" https://gyazo.com/ae77ab94a7eccb8f8c6603be45aa1020.png
curl -o "dist/assets/taylor.png" https://gyazo.com/a0c666e23c31024e4b5097f626d550e0.png
curl -o "dist/assets/rearranged.png" https://gyazo.com/f5846f1ed0e124ad66cb5690437a8cd8.png

python3 -m pip install --upgrade pip

python3 -m pip install --upgrade scipy
python3 -m pip install --upgrade networkx
python3 -m pip install --upgrade matplotlib
python3 -m pip install --upgrade tk
python3 -m pip install --upgrade sympy
python3 -m pip install --upgrade Pillow
python3 -m pip install --upgrade mpmath
python3 -m pip install --upgrade schemdraw==0.17
python3 -m pip install --upgrade pipwin
python3 -m pip install pathlib

pyinstaller gui.py Function.py FuncTypes.py GateTypes.py NotGateTypes.py RearrangeType.py Util.py --name "FUNSC --debug" --clean --onefile --icon "assets/frame0/UK logo-white.png" --add-data "assets/frame0/*.png;assets/frame0" --hidden-import=scipy --hidden-import=networkx --hidden-import=matplotlib --hidden-import=PIL --hidden-import=PIL._imagingtk --hidden-import=PIL._tkinter_finder --hidden-import=sympy --hidden-import=mpmath --hidden-import=tk --hidden-import=schemdraw --debug=imports
pyinstaller gui.py Function.py FuncTypes.py GateTypes.py NotGateTypes.py RearrangeType.py Util.py --name "FUNSC" --clean -w --onefile --icon "assets/frame0/UK logo-web.png" --splash "assets/frame0/UK ECE mark.png" --add-data "assets/frame0/*.png;assets/frame0" --hidden-import=scipy --hidden-import=networkx --hidden-import=matplotlib --hidden-import=PIL --hidden-import=PIL._imagingtk --hidden-import=PIL._tkinter_finder --hidden-import=sympy --hidden-import=mpmath --hidden-import=tk --hidden-import=schemdraw --debug=imports
read