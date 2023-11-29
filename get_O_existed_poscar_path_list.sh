#!/bin/bash

# POSCARファイルが存在するパスの一覧を取得（：第2引数を環境ごとのcif/ディレクトリのパスに書き換える）
python3 get_poscar_existed_path_list.py /mnt/ssd_elecom_black_c2c_480G/cif
# 元素種C, Oを含むPOSCARファイルが存在するパスを取得
python3 get_O_existed_poscar_path_list.py
