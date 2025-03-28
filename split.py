import random
import os

def split_dataset(dataset_root, output_dir, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1):

    files = [ file.split('.')[0] for file in os.listdir(dataset_root)]
    random.shuffle(files)

    total = len(files)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)

    train_files = files[:train_end]
    val_files = files[train_end:val_end]
    test_files = files[val_end:]
    trainval_files = train_files + val_files

    with open(f"{output_dir}/train.txt", 'w') as f:
        f.write('\n'.join(train_files))

    with open(f"{output_dir}/val.txt", 'w') as f:
        f.write('\n'.join(val_files))

    with open(f"{output_dir}/test.txt", 'w') as f:
        f.write('\n'.join(test_files))

    with open(f"{output_dir}/trainval.txt", 'w') as f:
        f.write('\n'.join(trainval_files))


# 使用示例
abspath_of_your_imagesfolder = "./aug_images"
split_dataset(abspath_of_your_imagesfolder, ".")