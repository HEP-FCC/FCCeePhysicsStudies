cwd=$PWD
cd $FCCANALYSES
#rm -rf build install
mkdir build install
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install
make install
cd $cwd
