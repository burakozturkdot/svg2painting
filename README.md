# svg2painting
Convert SVG vector graphics to paintings by rasterizing with brush textures

SVG2Painting           |  Standard Rendering
:---------------------:|:-------------------:
![](svg2painting.png)  |  ![](standard.png)

## Install requirements

```bash
pip install opencv-python
pip install numpy
pip install tqdm
pip install svgpathtools
```
## Basic Usage
`python svg2painting.py -i example.svg -o out.png -r 1024 -b 0`

### Additional options
`python svg2painting.py [-h] [-i INPUT_PATH] [-o OUTPUT_PATH] [-r RESOLUTION] [-b BRUSH] [-t BRUSH_DIRECTORY]`

|Argument| Description|
|:--|:--|
|`-h, --help`| Show this help message and exit.|
|`-i`| Input path. Specify the SVG file you want to be processed.|
|`-o`| Output path. Specify the location of the output file. (i.e. out.png)|
|`-r`| Image resolution. Specify the resolution of the longest side of output image. Aspect ratio will be choose automatically.|
|`-b`| Brush number. [0...44]|
|`-t`| Brush directory. Specify the path where all the brushes live.|
|`-s`| Number of samples per path. Set this higher if strokes don't look continous or lower if the runtime is to long.|

### Available Brushes
| | | | | | | | | | |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
<img src='brushes/SLOS_dry-point.png' width='150' height='150'> | <img src='brushes/SLOS_artist.png' width='150' height='150'> | <img src='brushes/SLOS_chalk.png' width='150' height='150'> | <img src='brushes/SLOS_charcoal-large.png' width='150' height='150'> | <img src='brushes/SLOS_watercolor.png' width='150' height='150'> | <img src='brushes/X_SLOS_lineline-3.png' width='150' height='150'> | <img src='brushes/SLOS_grass-1.png' width='150' height='150'> | <img src='brushes/SLOS_knife.png' width='150' height='150'> | <img src='brushes/SLOS_rectangle-1.png' width='150' height='150'> | <img src='brushes/SLOS_leafs.png' width='150' height='150'> | 
0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 
<img src='brushes/SLOS_fpStar.png' width='150' height='150'> | <img src='brushes/SLOS_triangle.png' width='150' height='150'> | <img src='brushes/SLOS_some-lines.png' width='150' height='150'> | <img src='brushes/SLOS_artist-1.png' width='150' height='150'> | <img src='brushes/X_SLOS_lineline-2a.png' width='150' height='150'> | <img src='brushes/SLOS_tree-bark.png' width='150' height='150'> | <img src='brushes/SLOS_texture-1.png' width='150' height='150'> | <img src='brushes/SLOS_many-nids.png' width='150' height='150'> | <img src='brushes/SLOS_writing-brush.png' width='150' height='150'> | <img src='brushes/SLOS_dry-pen.png' width='150' height='150'> | 
10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 
<img src='brushes/SLOS_br002.png' width='150' height='150'> | <img src='brushes/SLOS_lineline-1.png' width='150' height='150'> | <img src='brushes/SLOS_texture-2.png' width='150' height='150'> | <img src='brushes/SLOS_square-r.png' width='150' height='150'> | <img src='brushes/SLOS_br001.png' width='150' height='150'> | <img src='brushes/SLOS_fine-sand.png' width='150' height='150'> | <img src='brushes/SLOS_dry.png' width='150' height='150'> | <img src='brushes/SLOS_crayon.png' width='150' height='150'> | <img src='brushes/SLOS_moss-1.png' width='150' height='150'> | <img src='brushes/SLOS_granules.png' width='150' height='150'> | 
20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 
<img src='brushes/SLOS_twig.png' width='150' height='150'> | <img src='brushes/SLOS_blender.png' width='150' height='150'> | <img src='brushes/SLOS_pentagon.png' width='150' height='150'> | <img src='brushes/SLOS_lineline-2.png' width='150' height='150'> | <img src='brushes/SLOS_leafs-1.png' width='150' height='150'> | <img src='brushes/SLOS_rectangle.png' width='150' height='150'> | <img src='brushes/X_SLOS_parallel-lines.png' width='150' height='150'> | <img src='brushes/SLOS_charcoal.png' width='150' height='150'> | <img src='brushes/SLOS_hexagon.png' width='150' height='150'> | <img src='brushes/SLOS_br003.png' width='150' height='150'> | 
30 | 31 | 32 | 33 | 34 | 35 | 36 | 37 | 38 | 39 | 
<img src='brushes/SLOS_water-drop.png' width='150' height='150'> | <img src='brushes/SLOS_sewing.png' width='150' height='150'> | <img src='brushes/X_SLOS_parallel-lines-a1.png' width='150' height='150'> | <img src='brushes/SLOS_texture-dry.png' width='150' height='150'> | <img src='brushes/X_SLOS_parallel-lines-a2.png' width='150' height='150'> | 
40 | 41 | 42 | 43 | 44 | 

### References
- [SLOS-GIMPainter](https://github.com/SenlinOS/SLOS-GIMPainter): That's where all the brushes came from.
- [gimpFormats](https://github.com/TheHeadlessSourceMan/gimpFormats): Was used to convert the brushes to PNG.