@RD /S /Q build
@RD /S /Q dist

pyinstaller BackSeatGamerIRCRelay.py --onefile --name "IRCRelay" -i assets/logo.ico -y --clean --noconsole

cp assets dist -r

cd dist
zip -r "IRCRelayWindows.zip" *

PAUSE