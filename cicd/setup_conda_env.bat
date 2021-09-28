call conda update -y -n base -c defaults conda
call conda create -y -n alex python=3.9.*
call conda activate alex
call pip install -r ./tests/requirements.txt
call pip install -r requirements.txt