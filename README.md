# Orca-Prusa-Slicer-post-processing-scripts.
Simple scripts (very limited and incomplete hacks, really) to pass 3D printer slicer post-slicing info and gcode modifications forward to a final Ultimaker-compatible (or other printer) gcode file. Many other variables still need to be passed to realize the full potential of post-processing and I'm sorry that I don't program in Python (maybe someday). I'm now retired from the computer industry and cut my teeth on K&R C, Fortran, Pascal, and several assembly languages many decades ago. Accordingly, Python is Greek to me!

Both OrcaSlicer and PrusaSlicer can automatically launch the scripts to produce an Ultimaker-compatible gcode file output. Tested with an Ultimaker 3 using both memory stick ("sneaker net") and Cura/Ethernet gcode upload to the UM3.

I adapted Ultimaker_insert_time.py from https://github.com/MaciejWanat/ender-v3-prusa-preview-data (Accordingly, its MIT License appears here).

Other useful links.

User "Peace" ("MaciejWanat" on github):
https://forum.prusa3d.com/forum/original-prusa-i3-mk3s-mk3-hardware-firmware-and-software-help/using-variables-in-start-gcode/#post-788116

GUI Script to recover mysterious OrcaSlicer preset losses:
https://www.reddit.com/r/OrcaSlicer/comments/1qugcz4/saving_user_preset_from_project_doesnt_save_all/ 
I had to point the script to my ~/.var/app/com.orcaslicer.OrcaSlicer/ subdirectory. I'm using a Flatpak install and other subdirectory locations may vary.

Ultimaker S-Series profiles ("presets"):
https://ansonliu.com/2024/04/ultimaker-s3-s5-s7-prusaslicer-profile/

My work here barely scratches the surface of useful useful post-processing. I hope someone else who knows Python can run with it!
