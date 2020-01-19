# MCNP_AUTO

Automatic .i runner for MCNP

Place the folder containing auto.py into the same folder as your mcnp files

hierarchy should look like this


MCNP_Folder

   |
  
   |__> FileName.i
  
   |
  
    |__>FileName2.i
  
   |
  
   |__>MCNP_Runner
  
         |
         
         |__>auto.py
         
         |
         |__>ascension.py
         
         |
         
         |__>duel.mp3
         
         |
         
         |__>requirements.txt
         
         |
         
         |__>etc.
         
To run the .i files execute auto.py with  python either through terminal or by double clicking

        *I have not yet tested the program on mac
        
The program will 

  pip install all requirements,
  
  run all .i files contained in the higher level directory [FileName.i and FileName2.i],
  
  create or append keff.csv which will contain
  
    file name to the first "."| File name from first period to first "_"| keff| std dev
    
    a example file name that will work well is MOX.1.13_PitchRuns.i
    
    this will result in
    
    MOX|1.13|<KeffValue>|<Std.Dev>|
    
    being returned in the csv
    
Should one not wish to save the .r and .s files, one may uncomment the lines in auto.py which contain 

      # remove(name[:len(name)-1]+".r")
      
      # remove(name[:len(name)-1]+".s")
