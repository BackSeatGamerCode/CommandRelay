@RD /S /Q build
@RD /S /Q dist

pyinstaller BackSeatGamerCommandRelay.py --onefile --name "CommandRelay" -i assets/logo.ico -y --clean --noconsole

cp assets dist -r

cd dist
zip -r "CommandRelayWindows.zip" *

PAUSE