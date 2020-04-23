FROM raspbian/stretch

USER root
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install git -y

# INSTALL PYTHON 3.7.7
RUN apt-get install build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev -y \
    && wget https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tar.xz \
    && tar xf Python-3.7.7.tar.xz \
    && cd Python-3.7.7 \
    && ./configure \
    && make -j 4 \
    && make altinstall \
    && cd .. \
    && rm Python-3.7.7.tar.xz \
    && apt-get --purge remove build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev -y \
    && apt-get autoremove -y \
    && apt-get clean

# UPGRADE PIP
RUN apt-get install python3-pip -y \
    && pip3 install --upgrade pip

# INSTALL REQUIREMENTS 
COPY requirements.txt /
RUN pip install -r requirements.txt
