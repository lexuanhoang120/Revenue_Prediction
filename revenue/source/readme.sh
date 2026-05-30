

## vm ubuntu 16.04
icools - i
## vm ubuntu 14.04
icool - i

gene110/data:gvo_pro04 

path=/mnt/GSHD_DATA_01/partner/icool/revenue/source
docker run -it --rm -v $path:/source gene110/data:gvo_pro04 bash


python3     /source/main.py         \
--run       2021_01_08              \
--data      /source/data/DT.csv     \
--p         35                      \
--store     1                       \
--cutoff    2020-09-12


## 


cd /mnt/GVO/space/revenue
conda deactivate
source env/bin/activate

jupyter notebook --allow-root --no-browse



pip3 install sklearn
pip3 install jupyter notebook



##


path=/mnt/GSHD_DATA_01/partner/icool/revenue/source
docker run -it --net host -v $path:/source gene110/data:gvo_pro04 bash


python3     /source/main.py         \
--run       2021_01_08              \
--data      /source/data/DT.csv     \
--p         35                      \
--store     1                       \
--cutoff    2020-09-12





