import argparse
import numpy as np
from PIL import Image
import subprocess
import logging as log
import os


def is_valid_file(path):
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError("Not a valid file")
    return path


def create_assembly_code(im_frame, funcname, assembly_command, blocksize, export_function):

    LABEL = "PIXEL{}_{}"

    image_height = im_frame.shape[0]
    image_width = im_frame.shape[1]

    if export_function is True:
        assembly_data = """
        global {}
        export {}
        
        segment .text
        {}:
            mov eax, 0
            jmp [jmp_table_painter_row1 + eax*4]
        """.format(funcname, funcname, funcname)

    else:
        assembly_data = """
        global {}
    
        segment .text
        {}:
            mov eax, 0
            jmp [jmp_table_painter_row1 + eax*4]
        """.format(funcname, funcname)

    log.info("Creating the assembly code of the image.")
    for i in range(1, image_width + 1):
        for j in range(1, image_height + 1):
            curr_label = LABEL.format(str(j), str(i))
            assembly_data += curr_label + ":\n"
            # First Column.
            if i == 1:
                assembly_data += assembly_command * blocksize
            else:
                assembly_data += assembly_command * max(1, int(im_frame[j - 1, i - 1]) * blocksize)

            # Last Row then only jmp finish.
            if j == image_height:
                assembly_data += "\tjmp finish\n"

            # Middle Column, new jump table.
            elif i == int(image_width / 2) + 1:
                assembly_data += "\tjmp " + LABEL.format(str(j + 1), str(i)) + "\n"
            elif i < int(image_width / 2) + 1:
                assembly_data += "\tjz " + LABEL.format(str(j + 1), str(i + 1)) + "\n"
            elif i > int(image_width / 2) + 1:
                assembly_data += "\tjz " + LABEL.format(str(j + 1), str(i - 1)) + "\n"

    assembly_data += "finish:\n\tret\n"

    for i in range(1, image_width + 1):
        assembly_data += "jmp_table_painter_row{}:\n".format(str(i))

        for j in range(1, 2):  # ROWS + 1):
            curr_label = LABEL.format(str(j), str(i))
            assembly_data += "\tdd " + curr_label + "\n"

    return assembly_data

if __name__ == "__main__":

    BANNER = """
     █████     █████           █████   ███   █████                                 ██████                              
░░███     ░░███           ░░███   ░███  ░░███                                 ███░░███                             
 ░███   ███████   ██████   ░███   ░███   ░███   ██████   ████████   ██████   ░███ ░░░   ██████   ████████   ██████ 
 ░███  ███░░███  ░░░░░███  ░███   ░███   ░███  ░░░░░███ ░░███░░███ ███░░███ ███████    ░░░░░███ ░░███░░███ ███░░███
 ░███ ░███ ░███   ███████  ░░███  █████  ███    ███████  ░███ ░░░ ░███████ ░░░███░      ███████  ░███ ░░░ ░███████ 
 ░███ ░███ ░███  ███░░███   ░░░█████░█████░    ███░░███  ░███     ░███░░░    ░███      ███░░███  ░███     ░███░░░  
 █████░░████████░░████████    ░░███ ░░███     ░░████████ █████    ░░██████   █████    ░░████████ █████    ░░██████ 
░░░░░  ░░░░░░░░  ░░░░░░░░      ░░░   ░░░       ░░░░░░░░ ░░░░░      ░░░░░░   ░░░░░      ░░░░░░░░ ░░░░░      ░░░░░░
    
    By: Yoav Shaharabani
    https://github.com/yoavshah
"""
    print(BANNER)
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true')
    parser.add_argument("--path", dest='image_path', type=is_valid_file, help="Path to the image file (PNG, JPEG, JPG, BMP) to parse.", required=True)
    parser.add_argument("-b", "--blocksize", dest='block_size', type=int, default=10, help="Number of commands in each block.")
    parser.add_argument("-c", "--command", dest='assembly_command', type=str,
                        default="VFMADDSUB132PS xmm1, xmm2, cs:[edi + esi * 4+0x11111111]",
                        help="Assembly command to be filled with.")

    parser.add_argument("--funcname", dest='function_name', type=str, default="_main", help="Function name.")
    parser.add_argument('--obj', dest='create_objfile', default=True, action='store_true', help="Create Object File.")
    parser.add_argument('--exp', dest='export_function', default=False, action='store_true', help="Export function.")
    parser.add_argument("--asm_output", dest='asm_output', type=str, default="code.asm", help="Assembly file output.")
    parser.add_argument("--obj_output", dest='obj_output', type=str, default="code.obj", help="Object file output (Requires --obj flag).")

    args = parser.parse_args()

    if args.verbose:
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.INFO)
        log.info("Verbose output.")
    else:
        log.basicConfig(format="%(levelname)s: %(message)s")

    args.assembly_command = "\t" + args.assembly_command + "\n"

    log.info("Opening image file.")
    image_frame = Image.open(args.image_path)
    image_frame = np.asarray(image_frame.convert("1"))

    to_write = create_assembly_code(image_frame, args.function_name, args.assembly_command, args.block_size, args.export_function)

    log.info("Writing assembly output to file.")
    f = open(args.asm_output, "w")
    f.write(to_write)
    f.close()

    if args.create_objfile is True:
        log.info("Compiling assembly file to object file.")
        result = subprocess.run(["utils\\nasm.exe", "-f", "win32", args.asm_output, "-o", args.obj_output])
        if result.returncode != 0:
            log.error("Compiling assembly file to object file has failed.")
        else:
            log.info("Compiling assembly file to object file has finished successfully.")

    log.info("Program ended :) Enjoy.")
















    
