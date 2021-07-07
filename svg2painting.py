from svgpathtools import svg2paths
import xml.etree.ElementTree as ET
import cv2
import numpy as np
from tqdm import trange
import argparse
import os

def get_svg_sz(svg_in):
    tree = ET.parse(svg_in)
    root = tree.getroot()
    svg_h = int(root.attrib['height'])
    svg_w = int(root.attrib['width'])    
    
    return svg_h, svg_w

def get_strokes(svg_in, num_samples):
    paths, attributes = svg2paths(svg_in)
    strokes = []

    for i in range(len(paths)):
        p = paths[i]
        a = attributes[i]
        stroke = {}
        stroke['color'] = a['stroke'].replace('rgb(', '').replace(')', '').replace(' ', '').split(',')
        stroke['color'] = np.array(stroke['color']).astype(int)
        stroke['opacity'] = float(a['stroke-opacity'])
        stroke['width'] = float(a['stroke-width'])

        pts = []
        for j in range(num_samples):
            pt = np.array([paths[i].point(j/(num_samples-1)).real, paths[i].point(j/(num_samples-1)).imag])
            pts.append(pt)

        stroke['points'] = pts

        strokes.append(stroke)
        
    return strokes

def load_brushes(brushdir = 'brushes/'):
    brushfiles = os.listdir(brushdir + '/')
    brushes = []
    for f in brushfiles:
        if len(f.split('.png')) == 2:
            brush = cv2.imread(brushdir + f)
            if brush.shape[0] == brush.shape[1]:
                brushes.append(cv2.imread(brushdir + f))    
    return brushes

def angle(vec0, vec1=np.array([1,0])):
    # calculate angle of the stroke
    unit0 = vec0 / np.linalg.norm(vec0)
    unit1 = vec1 / np.linalg.norm(vec1)
    return np.arccos(np.dot(unit0, unit1))

def rotate_brush(image, angle):
    # rotate brush
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

def draw(strokes, brush, im_sz=(1024,1024), svg_sz=(256,256), rotate=False):
    im_w, im_h = im_sz
    svg_w, svg_h = svg_sz
    
    fac = [int(im_w/svg_w), int(im_h/svg_h)]
    fac_mid = int(abs(fac[0] + fac[1])/ 2)
    
    brush_w, brush_h, _ = brush.shape

    painting = np.ones([im_w, im_h, 3], dtype=np.uint8)*255

    for i in trange(len(strokes)):
        stroke = strokes[i]
        color = stroke['color'].tolist()
        width = int(stroke['width']*fac_mid)
        pts = stroke['points']
        opacity = stroke['opacity']

        overlay = np.copy(painting) #np.zeros([im_w, im_h, 3], dtype=np.uint8)#*255
                
        # draw strokes
        for j in range(len(pts)):
            dim = (width, width)
            p = pts[j]
            
            if j == 0:
                # resize brush and make it usable as a contour         
                brush_r = cv2.resize(np.copy(brush), dim, interpolation = None)#cv2.INTER_AREA)
                _, brush_r = cv2.threshold(brush_r,250,255,cv2.THRESH_BINARY)
                brush_r = cv2.cvtColor(brush_r, cv2.COLOR_BGR2GRAY)
                contours, hierarchy = cv2.findContours(~brush_r, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
                           
            # rotate brush every now and then            
            if rotate:
                if ((j+1) % 5) == 0:
                    #print("angled")
                    pvec = pts[j] - pts[j-1]
                    rad = angle(pvec)
                    brush_r = rotate_brush(np.copy(brush), rad)

                    # resize brush and make it usable as a contour         
                    brush_r = cv2.resize(brush_r, dim, interpolation = None)#cv2.INTER_AREA)
                    _, brush_r = cv2.threshold(brush_r,250,255,cv2.THRESH_BINARY)
                    brush_r = cv2.cvtColor(brush_r, cv2.COLOR_BGR2GRAY)
                    contours, hierarchy = cv2.findContours(~brush_r, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

            # draw the brush 
            coord = tuple(((p*fac).astype(int) - [width//2, width//2]).tolist())        
            cv2.drawContours(overlay, contours, -1, color, -1, offset=coord)

        painting = cv2.addWeighted(overlay, opacity, painting, 1 - opacity, 0)    
    
    return painting

def main():
    parser = argparse.ArgumentParser(description = "Render SVG Vector Graphics as Paintings.")
    parser.add_argument("-i", metavar="INPUT_PATH", default="example.svg",
                        help="Input path. Specify the SVG file you want to be processed.")
    parser.add_argument("-o", metavar="OUTPUT_PATH", default="out.png",
                        help="Output path. Specify the location of the output file. (i.e. out.png)")
    parser.add_argument("-r", metavar="RESOLUTION", type=int, default=1024,
                        help="Image resolution. Specify the resolution of the longest side of output image. Aspect ratio will be choose automatically.")
    parser.add_argument("-b", metavar="BRUSH", type=int, default=0,
                        help="Brush number. [0...44]")    
    parser.add_argument("-t", metavar="BRUSH_DIRECTORY", default='brushes/',
                        help="Brush directory. Specify the path where all the brushes live.")
    parser.add_argument("-s", metavar="SAMPLE_POINTS", type=int, default=1000,
                        help="Number of samples per path. Set this higher if strokes don't look continous or lower if the runtime is to long.")    
    
    args = parser.parse_args()

    svg_in = args.i
    img_out = args.o
    res_max = args.r
    brush_dir = args.t
    brush_i = args.b
    num_samples = args.s
    
    print("Load SVG and brushes")
    svg_sz = get_svg_sz(svg_in)
    ratio = np.max(svg_sz) / np.min(svg_sz)
    im_sz = [res_max, res_max]
    im_sz[np.argmin(svg_sz)] = int(res_max/ratio)
    
    strokes = get_strokes(svg_in, num_samples)    
    brushes = load_brushes(brush_dir)
    
    print("Start drawing...")
    painting = draw(strokes, brushes[brush_i], im_sz=im_sz, svg_sz=svg_sz)

    out = cv2.cvtColor(painting, cv2.COLOR_RGB2BGR)
    cv2.imwrite(img_out, out)
    print("Done.")
    
if __name__ == "__main__":
    main()    