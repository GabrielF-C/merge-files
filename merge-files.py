import argparse
import filecmp
from io import TextIOWrapper
import os


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--inputs", required=True, nargs="+", help="<Required> list of files to merge")
ap.add_argument("-o", "--output", required=True, type=str, help="<Required> path to the output file")
ap.add_argument("-b", "--backup", type=str, help="path to backup directory")
ap.add_argument("-ie", "--input-extension", type=str, help="if specified, input files must end with this extension")
ap.add_argument("-oe", "--output-extension", type=str, help="if specified, output path must end with this extension")
args = ap.parse_args()

# -----------------------------------------------------------

def main(input_file_paths: list, input_extension: str, output_file_path: str, output_extension: str, backup_dir_path: str):
  def get_backup_path():
    return f"{backup_dir_path}/{output_file_path}.backup"

  def get_backup_backup_path():
    return f"{backup_dir_path}/{output_file_path}.backup.backup"

  def preprocess_output_file():
    if output_extension and not output_file_path.lower().endswith(output_extension):
      raise ValueError(f"Output does not end with the following extension : {output_extension}")

    print("Backup of the old output will be created (older backup will be overwritten)")

    output_backup_path = get_backup_path()
    output_backup_backup_path = get_backup_backup_path()

    if os.path.isfile(output_backup_path):
      os.replace(output_backup_path, output_backup_backup_path)

    if os.path.isfile(output_file_path):
      os.rename(output_file_path, output_backup_path)

    return open(output_file_path, "a+")


  def restore_output_backup():
    print("Restoring old output file and backups")

    output_backup_path = get_backup_path()
    output_backup_backup_path = get_backup_backup_path()

    if os.path.isfile(output_file_path):
      os.remove(output_file_path)

    if os.path.isfile(output_backup_path):
      os.rename(output_backup_path, output_file_path)

    if os.path.isfile(output_backup_backup_path):
      os.rename(output_backup_backup_path, output_backup_path)


  def postprocess_output_file():
    print("Cleaning up")

    output_backup_backup_path = get_backup_backup_path()

    if (os.path.isfile(output_backup_backup_path)):
      os.remove(output_backup_backup_path)

  def process():
    if len(input_file_paths) < 2:
      raise ValueError("Must provide multiple inputs to merge")
    if not os.path.isdir(backup_dir_path):
      os.mkdir(backup_dir_path)

    print("Merging the following files : \n\t" + "\n\t".join(input_file_paths))
    print("Output file : \n\t" + output_file_path)

    output_file = preprocess_output_file()

    try:
      for input_file_path in input_file_paths:
        process_input_file(input_file_path, input_extension, output_file)
    except Exception as e:
      output_file.close()
      restore_output_backup()
      raise e
    else:
      output_file.close()
      output_backup_path = get_backup_path()
      if os.path.isfile(output_backup_path) and filecmp.cmp(output_file_path, output_backup_path, shallow = False):
        print("Resulting output is same as the old one")
        restore_output_backup()
      else:
        postprocess_output_file()
  # -----------------------------------------------------------
  process()
  # -----------------------------------------------------------

  
def process_input_file(input_file_path: str, input_extension: str, output_file: TextIOWrapper):
  if input_extension and not input_file_path.lower().endswith(input_extension):
    raise ValueError(f"Input '{input_file_path}' must end with the following extension : {input_extension}")
  
  if not os.path.isfile(input_file_path):
    raise FileNotFoundError(f"Input '{input_file_path}' does not exist")
  input_file = open(input_file_path)
  output_file.write(input_file.read() + "\n")
  input_file.close()

# =============================================================

if __name__ == '__main__':
  main(args.inputs, args.input_extension, args.output, args.output_extension, args.backup or ".")