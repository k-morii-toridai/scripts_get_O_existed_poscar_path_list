import os
from pathlib import Path
from multiprocessing import Pool, cpu_count

from tqdm import tqdm
import numpy as np


# poscar_abs_path_listをload
poscar_abs_path_list_loaded = np.load('poscar_existed_file_path_list.npy', allow_pickle=True)
print(f"len(poscar_abs_path_list_loaded): {len(poscar_abs_path_list_loaded)}")


def return_O_exist(poscar_path):
    def get_species_from_poscar(poscar_path):
        # POSCARファイルから元素種の行から元素種を取り出す
        with open(poscar_path, mode='r') as f:
            poscar_line_list = f.readlines()
            # poscarからspeciesをリストで取得
            species_list = set(poscar_line_list[5][:-1].split(' '))
            species_list.discard('')
            return species_list

    return set(['O']) <= set(get_species_from_poscar(poscar_path))


# return_O_exist()を並列化して実行
p = Pool(cpu_count() - 1)
bool_O_exist_list = list(tqdm(p.imap(return_O_exist, poscar_abs_path_list_loaded), total=len(poscar_abs_path_list_loaded)))
p.close()
p.join()

# CとOを含むPOSCARファイルを抽出し，そのリストを.npy形式で保存
O_existed_poscar_file_path_list = poscar_abs_path_list_loaded[bool_O_exist_list]
print(f"len(O_existed_poscar_file_path_list): {len(O_existed_poscar_file_path_list)}")
np.save('O_existed_poscar_file_path_list.npy', O_existed_poscar_file_path_list)
# CとOを含むPOSCARファイルのフォルダのリストを.npy形式で保存
O_existed_poscar_folder_path_list = [Path(os.path.split(p)[0]) for p in O_existed_poscar_file_path_list]
np.save('O_existed_poscar_folder_path_list.npy', O_existed_poscar_folder_path_list)
print("O_existed-poscar file, and folder path list were saved as .npy!!!")
