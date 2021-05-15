import numpy as np
import math
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

WPFILE="reinvent_base.npy"
OUTFILE='2018.svg'
AIFILE='2018.ai'
ANGLE=0.22
CENTERX=360
CENTERY=300
OFFSETX=-50
OFFSETY=50
CANVASH=600
CANVASW=720
FIRSTLINE=True
SECONDLINE=True


def Nrotate(angle,valuex,valuey,pointx,pointy,offsetx,offsety):
  valuex = np.array(valuex)
  valuey = np.array(valuey)
  nRotatex = (valuex-pointx)*math.cos(angle) - (valuey-pointy)*math.sin(angle) + pointx + offsetx
  nRotatey = (valuex-pointx)*math.sin(angle) + (valuey-pointy)*math.cos(angle) + pointy + offsety
  nRotatex=np.round(nRotatex*10)/10
  nRotatey=np.round(nRotatey*10)/10
  return nRotatex, nRotatey

def getPoly(c,colorStr, edgeColor, swidth, extraStyle):
	c=c*1000
	c=np.round(c)/10
	#print(c)
	c_shape=c.shape
	c_length=c_shape[0]
	#print(c_length)
	c_polygon='<polygon points="'
	for i in range(c_length):
		y_mirror=np.round(500-c[i][1])
		rx,ry=Nrotate(ANGLE,c[i][0],y_mirror,CENTERX,CENTERY,OFFSETX,OFFSETY)
		c_polygon=c_polygon+str(rx)+','+str(ry)+' '
	c_polygon=c_polygon+'" style="fill:' + colorStr + '; stroke-linejoin:bevel; stroke:'+edgeColor+'; stroke-width:'+str(swidth)+';'+extraStyle+'"/>\n'
	#print(c_polygon)
	return c_polygon

def getStartPoly(c_begin,c_end, edgeColor, swidth, extraStyle):
	c_begin=c_begin*1000
	c_begin=np.round(c_begin)/10
	c_end=c_end*1000
	c_end=np.round(c_end)/10

	#print(c_length)
 
	c_line='<line x1="'
	y_mirror=np.round(500-c_begin[1])
	rx,ry=Nrotate(ANGLE,c_begin[0],y_mirror,CENTERX,CENTERY,OFFSETX,OFFSETY)	
	c_line=c_line+str(rx)+'" y1="'+str(ry)+'" x2="'
	y_mirror=np.round(500-c_end[1])
	rx,ry=Nrotate(ANGLE,c_end[0],y_mirror,CENTERX,CENTERY,OFFSETX,OFFSETY)
	c_line=c_line+str(rx)+'" y2="'+str(ry)+'" style=" stroke:'+edgeColor+'; stroke-width:'+str(swidth)+';'+extraStyle+'"/>\n'
	print(c_line)
	return c_line

# Load the center, inner, outer waypoints
waypoints = np.load(WPFILE)
waypoints_shape=waypoints.shape
waypoints_length=waypoints_shape[0]-1
waypoints_length_half=int(np.round(waypoints_length/2))
print(waypoints_length_half)


with open(OUTFILE, 'w') as the_file:
    the_file.write('<svg xmlns="http://www.w3.org/2000/svg" width="'+str(CANVASW)+'" height="'+str(CANVASH)+'">\n')
    the_file.write('<rect width="'+str(CANVASW)+'" height="'+str(CANVASH)+'" style="fill:#00C491" />\n')
    the_file.write(getPoly(0.1*waypoints[:,0:2]+0.9*waypoints[:,4:6],'black','white',7.5, " "))
    the_file.write(getPoly(0.1*waypoints[:,0:2]+0.9*waypoints[:,2:4],'#00C491', 'white', 7.5, " "))
    the_file.write(getPoly(waypoints[:,0:2],'none', '#ff9f00', 2.5, " stroke-dasharray:5 ; "))
    if FIRSTLINE:
    	the_file.write(getStartPoly(waypoints[0,2:4],waypoints[0,4:6], 'white', 5,  " stroke-dasharray:5 ; "))
    	if SECONDLINE:
    		the_file.write(getStartPoly(waypoints[waypoints_length_half,2:4],waypoints[waypoints_length_half,4:6], 'white', 5,  " stroke-dasharray:5 ; "))
    the_file.write('</svg>')

#getStartPoly(waypoints[0,2:4],waypoints[0,4:6], 'white', 5,  " stroke-dasharray:10 ; ")

drawing = svg2rlg(OUTFILE)
renderPDF.drawToFile(drawing, AIFILE)
