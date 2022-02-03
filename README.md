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


  ## Credits
  Real thanks for xoreaxeaxeax for the inspiration from his [project](https://github.com/xoreaxeaxeax/REpsych)


