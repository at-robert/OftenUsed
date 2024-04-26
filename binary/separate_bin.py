def split_binary(input_file, chunk_size):
  """
  Splits a binary file into chunks of a specified size.

  Args:
      input_file: Path to the input binary file.
      chunk_size: Size of each chunk in bytes.
  """
  with open(input_file, 'rb') as infile:
    part_number = 1
    while True:
      chunk = infile.read(chunk_size)
      if not chunk:
        break
      output_file = f"{input_file.split('.')[0]}_{part_number:03d}.bin"
      with open(output_file, 'wb') as outfile:
        outfile.write(chunk)
      part_number += 1

# Example usage
input_file = "hdcp2_2_msd92q_20210803_30K_001.bin"
# chunk_size = 1024 * 1024  # 1 MB chunks
chunk_size = 1044

split_binary(input_file, chunk_size)

print(f"Successfully split {input_file} into chunks of {chunk_size} bytes.")