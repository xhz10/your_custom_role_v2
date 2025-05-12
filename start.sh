pip3 install fastapi uvicorn
pip3 install virtualenv
virtualenv role-play
virtualenv -p python3.12 role-play
source role-play/bin/activate
crewai install
pip3 install -e .


cd src/your_custom_role_v2


nohup python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 9265 > out.log 2>&1 &
