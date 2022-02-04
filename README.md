# IdaWarfare

  ## IdaWarfare is a project allow you to create images inside IDA graph view using comfortable and dynamic arguments.

  ## Usage
  
  * Create an image (Any format accepted).
  * Feed the image to the script with the default parameters.
  * Throw the processed object file to Visual Studio.
  * Build with x86
  
  ## Notes
  
  * To change the function name of the image use the "--funcname" argument (Default is "_main").
  * To add the function to the exports table use the "--exp" flag.

  ## Usage Example
  
  * Run the command "python ida_warefare.py --path YS.png --obj --asm_output images\code.asm --obj_output images\code.obj -v".
  * Put the file "code.obj" into your Visual Studio project.

<img align="center" src="https://raw.githubusercontent.com/yoavshah/IdaWarfare/master/images/YS_VisualStudio.png" />

  * Build and open in IDA :)

<img align="center" src="https://raw.githubusercontent.com/yoavshah/IdaWarfare/master/images/YS_IDA.png" />


  ## How does it works?
  
  * Each code block is responsible to imitate an image pixel.
  * The project creates an assembly code that contains a jump table to the first row of code blocks, which corresponds to the first row of pixels in the image.
  * Each code block(image pixel) connects to the two pixels beneath him.
  * The last row of code blocks have a single jmp operator to the end of the function.
  * A black pixel have a numerous assembly instructions in its code block, A white pixel has only one assembly instruction.

  ## Credits
  Real thanks for xoreaxeaxeax for the inspiration from his [project](https://github.com/xoreaxeaxeax/REpsych)


