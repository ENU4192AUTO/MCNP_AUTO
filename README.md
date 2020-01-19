# MCNP_AUTO
Automatic .i runner for MCNP \n
Place the folder containing auto.py into the same folder as your mcnp files \n
hierarchy should look like this \n
MCNP_Folder\n
  | \n
  |__> FileName.i\n
  |\n
  |__>FileName2.i\n
  |\n
  |__>MCNP_Runner\n\n
         |\n
         |__>auto.py\n
         |\n
         |__>ascension.py\n
         |\n
         |__>duel.mp3\n
         |\n
         |__>requirements.txt\n
         |\n
         |__>etc.\n
To run the .i files execute auto.py with  python either through terminal or by double clicking\n
        *I have not yet tested the program on mac\n
The program will \n
  pip install all requirements,\n
  run all .i files contained in the higher level directory [FileName.i and FileName2.i],\n
  create or append keff.csv which will contain\n
    file name to the first "."| File name from first period to first "_"| keff| std dev\n
    a example file name that will work well is MOX.1.13_PitchRuns.i\n
    this will result in\n
    MOX|1.13|<KeffValue>|<Std.Dev>|\n
    being returned in the csv\n
Should one not wish to save the .r and .s files, one may uncomment the lines in auto.py which contain \n
      # remove(name[:len(name)-1]+".r")\n
      # remove(name[:len(name)-1]+".s")\n
