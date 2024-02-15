# pngtoplt
converts a. png file of a qr code into a .plt file

uses python and cv2 for the conversion
create a virtual environment, activate it, install cv2 and run the python script...

```
python main.py "input_file_name.png" "output_file_name.plt"
```

tailor made for a client, and contains a hard coded variable for the dimension of the qr code

adjust the variables in the python script as per your needs...

```
block_size = 10
gap = 4
qr_grid_factor = 6
```

