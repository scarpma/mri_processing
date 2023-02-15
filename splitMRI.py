import pydicom
import glob
import numpy as np
import tqdm
import shutil
import os
import sys
import os.path as osp

def get_subdir_names(patient_directory):
  dir_ = patient_directory
  cartelle_dentro = glob.glob(dir_ + "*/")
  
  while len(cartelle_dentro) != 4:
    assert len(cartelle_dentro) == 1, cartelle_dentro
    dir_ = osp.join(dir_, cartelle_dentro[0])  
    cartelle_dentro = glob.glob(dir_ + "*/")
  
  ch_names = []
  for dir_ in cartelle_dentro:
    if "SI" in dir_:
      assert "SI" not in ch_names
      ch_names.append("SI")
    elif "FH" in dir_:
      assert "FH" not in ch_names
      ch_names.append("FH")
    elif "AP" in dir_:
      assert "AP" not in ch_names
      ch_names.append("AP")
    elif "RL" in dir_:
      assert "RL" not in ch_names
      ch_names.append("RL")
    else:
      assert "mag" not in ch_names
      ch_names.append("mag")
  
  for ch, dir in zip(ch_names, cartelle_dentro):
    print(f"{ch:5} -->   {dir}")
    
  return cartelle_dentro, ch_names






if __name__ == "__main__":

    assert len(sys.argv) == 2, "one argument must be provided"
    patient_directory = osp.abspath(sys.argv[1])
    if patient_directory[-1] == "/":
        patient_directory = patient_directory[:-1]
    odir = patient_directory + "_"
    patient_directory = patient_directory + "/"
    directories, ch_names = get_subdir_names(patient_directory)
    
    # phase number: (2001,1008)
    
    for kk, directory in enumerate(directories):
    
      ch_name = ch_names[kk]
      filenames = glob.glob(directory+"*.dcm")
      assert len(filenames) > 1
      
      dcms = []
      for i in tqdm.tqdm_notebook(range(len(filenames))):
        dcms.append(pydicom.dcmread(filenames[i], specific_tags=[(0x2001,0x1008)]))
    
      pos = [int(dcm[0x2001,0x1008].value) for dcm in dcms]
      nPhases = max(pos) - min(pos) + 1
    
      print(f"ch_name: {ch_name}, nPhases: {nPhases}, nSlices: {len(dcms[1])}")
      dcms_ = {}
    
      for i in range(len(dcms)):
        if pos[i] in dcms_:
          dcms_[pos[i]].append(filenames[i])
        else:
          dcms_[pos[i]] = [filenames[i]]
    
      for k, v in tqdm.tqdm_notebook(dcms_.items()):
        print()
        output_dir = osp.join(odir, str(k).zfill(3), ch_name)
        os.makedirs(output_dir, exist_ok=True)
        for i in range(len(v)):
          #print(f"saving {v[i]}")
          shutil.copyfile(v[i], osp.join(output_dir, osp.basename(v[i])))
