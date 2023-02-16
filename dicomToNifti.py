import os.path as osp
import slicer
import glob

def convertToNifti(dicomFilesDirectory, outputPath):
    random_file = glob.glob(osp.join(dicomFilesDirectory, "*.dcm"))[0]
    node = slicer.util.loadVolume(random_file, {"singleFile": False})
    # Save node
    print(f'Write {node.GetName()} to {outputPath}')
    success = slicer.util.saveNode(node, outputPath)
    slicer.mrmlScene.Clear()
    return


patient_dir = "/home/bcl/mri_"
phaseNumbers = [dir.split("/")[-2] for dir in glob.glob(osp.join(patient_dir, "*/"))]
print(f"phaseNumbers found: {phaseNumbers}")



channel_names = ["mag", "RL", "AP", "FH"]

for phaseNumber in phaseNumbers:
    for channel_name in channel_names:
        dicomFilesDirectory = osp.join("/home/bcl/Martino/aorta_segmentation_v3/", patient_dir, phaseNumber, channel_name)
        print(dicomFilesDirectory)
        outputFolder = osp.join("/home/bcl/Martino/aorta_segmentation_v3/", patient_dir, channel_name)
        filename = phaseNumber + ".nii.gz"
        outputPath = osp.join(outputFolder, filename)
        convertToNifti(dicomFilesDirectory, outputPath)
