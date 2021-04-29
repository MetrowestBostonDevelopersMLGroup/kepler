################################################
# Because the project is pure python with few other dependencies
# it is possible to run on just a laptop (windows) PC. 
# This powershell scripts sets up the PYTHONPATH env variabls and loads all the
# python modules (libraries) into a venv/ folder.  This is
# referred to as a python "virtual environment" and essentially locks down
# the python library versions 
#
# This is windows (powershell) specific.  The linux shell script is almost identical.

# reference:   https://packaging.python.org/tutorials/installing-packages/#optionally-create-a-virtual-environment

# if venv folder does not exist - create it
if (-NOT (Test-Path '.\venv\Scripts\activate' -PathType Leaf)) {

    " "
    "did not find venv\Scripts\activate - creating now..."

    # confirm at least we have python with pip
    python --version
    python -m pip --version


    # create an empty virtualenv
    python -m venv venv

    }

# activate the venv
.\venv\Scripts\activate

# ensure pip, setuptools and wheels are up to date
python -m pip install --upgrade pip setuptools wheel

# get the libraries specified in requirements.txt and show a list
pip install -r requirements.txt
pip list


################################################
# add to PYTHONPATH for python modules
$Env:PYTHONPATH= '.'
$Env:PYTHONPATH= $Env:PYTHONPATH + ';' + $PSScriptRoot + ';'
$Env:PYTHONPATH= $Env:PYTHONPATH + ';' + $PSScriptRoot + '.\tests;'
$Env:PYTHONPATH= $Env:PYTHONPATH + ';' + $PSScriptRoot + '.\venv\Lib\site-packages;'


#################################################
# print instructions on what to do next...
" "
"Environment setup is complete.  Next step: start vs-code IDE using 'code-n .' "
" "
