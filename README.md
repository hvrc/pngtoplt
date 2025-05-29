# pngtoplt

Converts a .png file of a qr code into a .plt file

Tailor made for a client, using it for engraving license plates with qr codes alongside a laser engraver and [HP-GL](https://en.wikipedia.org/wiki/HP-GL).

Contains a hard coded variable for the dimension of the qr code.

Extracting and running the executable starts a process that continuously looks for a .png file being dropped into the executable's folder. 

When dropped, it deletes the .png and creates a .plt file in it's place. To be used alongside HPGL

To run it as a script with custom dimensions:

Create a virtual environment, activate it, install cv2 and run the python script...

```
python main.py "input_file_name.png" "output_file_name.plt"
```

adjust the variables in the python script as per your needs...

```
block_size = 10
gap = 4
qr_grid_factor = 6
```

## Screenshots

<div style="display: flex; gap: 10px;">
    <img src="images/readme_1.png" height="350">
    <img src="images/readme_2.PNG" height="350">
    <img src="images/readme_3.png" height="350">
</div>

